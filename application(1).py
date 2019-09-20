import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Shows concise record of a user's stock record"""
    # Selects stock that user actually has
    stockuserhas = db.execute(
        "SELECT symbol, shares FROM portfolio WHERE userid = :userid GROUP BY symbol HAVING SUM(shares) > 0", userid=session["user_id"])
    # Finds the amount of money user has to spend on stocks
    amount = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])
    # The virst value in the array is the amount of money user can spend
    money = amount[0]["cash"]
    # If the user does not have any stocks, return index using with just money as input
    if not stockuserhas:
        return render_template("index.html", money=money, completetotal=money)

    # Selects summarative information for each symbol
    stocks = db.execute(
        "SELECT SUM(total), symbol, SUM(shares), name FROM portfolio WHERE userid = :userid GROUP BY symbol", userid=session["user_id"])
    # For each symbol, add the current price of the stock to the end of the dictionary
    for stock in stocks:
        # Looks up current price of stock based on symbol
        stockinfo = lookup(stock["symbol"])
        # Finds current value of stock
        currentprice = float(stockinfo["price"])
        # Adds the price to the dictionary
        stock.update({"price": currentprice})

    # The total value of stocks user owns
    totalstockvalue = db.execute("SELECT SUM(total) FROM portfolio WHERE userid = :userid", userid=session["user_id"])
    # Total amount a user owns is the cash they have plus the sum of the stocks
    completetotal = float(money + float(totalstockvalue[0]['SUM(total)']))
    # Return index.html with all of the information put together above
    return render_template("index.html", completetotal=completetotal, money=money, stocks=stocks)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensures symbol was submitted
        if not request.form.get("symbol"):
            return apology("Must provide symbol", 400)
        # Ensures shares was submitted
        if not request.form.get("shares"):
            return apology("Must provide amount of shares", 400)
        # Ensures what is inputed for shares is numeric
        if not request.form.get("shares").isdigit():
            return apology("Must provide a valid amount of shares", 400)

        # Sets quote to the information about symbol inputed by user
        quote = lookup(request.form.get("symbol"))
        # Ensures symbol is a valid symbol that has a quote
        if not quote:
            return apology("Symbol invalid", 400)
        # Cost of stock
        cost = quote["price"]
        # Symbol of stock
        symbol = quote["symbol"]
        # Name of stock
        name = quote["name"]
        # Finds the amount of money user has to spend on stocks
        amount = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])
        # The virst value in the array is the amount of money user can spend
        money = amount[0]["cash"]
        # Total amount of money needed to buy the amount and type of stock user has inputed
        total = float(request.form.get("shares")) * cost
        # If user is able to afford the stock(s), update the cash colomn and add info to portfolio table
        if money >= total:
            # Remaining is the amount of cash a user has left after buying the stock
            remaining = money - total
            # Inserts amount remaining into the cash field
            db.execute("UPDATE users SET cash = ':remaining' WHERE id=:userid", remaining=remaining, userid=session["user_id"])
            # Logs stock transaction in portfolio
            db.execute("INSERT INTO portfolio (userid, symbol, price, shares, TOTAL, transacted, name) VALUES(:userid, :symbol, :price, :shares, :TOTAL, :transacted, :name)",
                        userid=session["user_id"], symbol=symbol, price=cost, shares=request.form.get("shares"), TOTAL=total, transacted=datetime.datetime.now(), name=name)

        # If user cannot afford stock(s), return apology
        else:
            return apology("You do not have enough money", 400)

        # Return back to index page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # Sets variable username to username inputed by user
    username = request.args.get("username")
    # Selects userid from username inputed by user (if there is one)
    userinfo = db.execute("SELECT * FROM users WHERE username = :username", username=username)
    # If there is no info on the username inputed, that means username is not taken, and user can take the username
    if not userinfo:
        # Return true for the username is not taken
        return jsonify(True)
    # Return false if there is info on the username (meaning it was taken)
    return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Select stock info for every single stock transaction for the respective user
    rows = db.execute("SELECT symbol, shares, price, transacted FROM portfolio WHERE userid = :userid", userid=session["user_id"])
    # Return template with the list that has each stock transaction info
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # If user submits a symbol
    if request.method == "POST":
        # If the user hits submit button without inputting symbol, return apology
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        # Sets quote to the information about symbol inputed by user
        quote = lookup(request.form.get("symbol"))
        # Ensures symbol is a valid symbol that has a quote, otherwise return apology
        if not quote:
            return apology("Symbol Invalid", 400)
        # Creates a list for the stock info that will be on display in html
        quoteinfo = [quote["name"], quote["symbol"], float(quote["price"])]
        # Returns page with the symbol's information inserted in it
        return render_template("quoted.html", quoteinfo=quoteinfo)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted, otherwise return apology
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted, otherwise return apology
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match, otherwise return apology
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        # Encrypts password inputed by user
        hash = generate_password_hash(request.form.get("password"))

        # Inserts encrypted password and username into database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hash)
        # Checks to make sure the username user inputed is unique, otherwise return apology
        if not result:
            return apology("Username is not available")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("registration.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensures symbol was submitted, otherwise return apology
        if not request.form.get("symbol"):
            return apology("must provide username", 400)
        # Ensures shares was submitted, otherwise return apology
        if not request.form.get("shares"):
            return apology("must provide username", 400)
        # The symbol user selected
        symbolselected = request.form.get("symbol")
        # The amount of shares of the stock user inputed
        amtshares = db.execute("SELECT SUM(shares), symbol FROM portfolio WHERE userid = :userid GROUP BY :symbol",
                                userid=session["user_id"], symbol=symbolselected)
        # Get the int version of how many shares person currently has
        amtshares = int(amtshares[0]["SUM(shares)"])

        # Amount of shares user wants to sell (it's negative because it reduces amount of shares user has for the stock)
        sharesinputed = -int((request.form.get("shares")))
        # If user does not have enough stock to sell with inputed amount of shares, return apology
        if (amtshares + sharesinputed) < 0:
            return apology("You do not have enough shares", 400)

        # Sets quote to the information about symbol inputed by user
        quote = lookup(request.form.get("symbol"))
        # Ensures symbol is a valid symbol that has a quote
        if not quote:
            return apology("Symbol Invalid", 400)
        # Amount of money stock will sell for
        value = quote["price"]
        # Name of stock
        name = quote["name"]
        # Total amount of money needed to buy the amount and type of stock user has inputed
        total = (value * sharesinputed)

        # Inserts sell transaction record into portfolio
        db.execute("INSERT INTO portfolio (userid, symbol, price, shares, TOTAL, transacted, name) VALUES(:userid, :symbol, :price, :shares, :TOTAL, :transacted, :name)",
                    userid=session["user_id"], symbol=symbolselected, price=value, shares=sharesinputed, TOTAL = total, transacted=datetime.datetime.now(), name=name)

        # Finds the amount of money user has to spend on stocks
        amount = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])
        # The virst value in the array is the amount of money user can spend
        money = amount[0]["cash"]
        # Final money count after adding value of stock (subtraction is used since total is negative, and we are adding sales value to cash)
        finalcashamount = money - total
        # Updates cash for user
        db.execute("UPDATE users SET cash = :finalcashamount WHERE id=:userid",
                    finalcashamount=finalcashamount, userid=session["user_id"])
        # Redirects user to index page
        return redirect("/")
    # If user is accessing sell page
    else:
        # List of symbols (not repeating)
        symbols = db.execute("SELECT symbol FROM portfolio WHERE userid = :userid GROUP BY symbol", userid=session["user_id"])

        # Returns sell.html with different types of symbols
        return render_template("sell.html", symbols=symbols)


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Changes user's password"""
    # If user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure new password was submitted, otherwise return apology
        if not request.form.get("passwordchange"):
            return apology("Must provide new password", 400)

        # Ensure confirmation was submitted, otherwise return apology
        elif not request.form.get("passwordchange(again)"):
            return apology("Must Give Password Verification", 400)

        # Ensure new password and confirmation match, otherwise return apology
        if request.form.get("passwordchange") != request.form.get("passwordchange(again)"):
            return apology("Passwords do not match", 400)

        # Encrypts password
        hash = generate_password_hash(request.form.get("passwordchange"))

        # Updates user's encrypted password
        db.execute("UPDATE users SET hash = :hash WHERE id=:userid", hash=hash, userid=session["user_id"])
        # Redirects user to index page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password_change.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
