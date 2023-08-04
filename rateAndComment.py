import click
from db import get_db_connection

@click.pass_context
def comment_as_renter(ctx, bookingId):
    sql_query = "SELECT * FROM BookedBy WHERE bookingId = %s AND renterSIN = %s"
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(sql_query, (bookingId, ctx.obj["userSIN"]))
    result = db_cursor.fetchone()
    if result is None:
        click.echo("Invalid booking ID.")
        return
    if result[5] ==1:
        click.echo("You have cancelled this booking.")
        return
    listingID =  result[1]
    renter_sin = result[2]
    sql_query = " SELECT * FROM UserCreatesListing WHERE listingId = %s"
    db_cursor.execute(sql_query, (listingID,))
    result = db_cursor.fetchone()
    if result is None:
        click.echo("Invalid listing ID.")
        return
    host_sin = result[0]

    sql_query = "INSERT INTO UserReviews (commentedOn, commentedBy, comment, rating) VALUES (%s, %s, %s, %s)"
    comment = click.prompt("Please enter a comment about the user.", type=str, default="", show_default=False)
    if comment == "":
        comment = None
    rating = click.prompt("Please enter a rating from 1 to 5",type=int)
    if rating == "":
        rating = None
    elif rating < 1 or rating > 5:
        click.echo("Invalid rating.")
        return
    db_cursor.execute(sql_query, (host_sin, renter_sin, comment, rating))
    db_connection.commit()
    db_cursor.close()
    click.echo("Thank you for your rating and comment.")


@click.pass_context
def comment_as_host(ctx,bookingid):
    sql_query = "SELECT * FROM BookedBy WHERE bookingId = %s"
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(sql_query, (bookingid,))
    result = db_cursor.fetchone()
    if result is None:
        click.echo("Invalid booking ID.")
        return
    if result[5] ==1:
        click.echo("You have cancelled this booking.")
        return
    renterSin = result[2]
    listingID =  result[1]
    sql_query = " SELECT * FROM UserCreatesListing WHERE listingId = %s"
    db_cursor.execute(sql_query, (listingID,))
    result = db_cursor.fetchone()
    if result is None:
        click.echo("Invalid listing ID.")
        return
    host_sin = result[0]
    if host_sin != ctx.obj["userSIN"]:
        click.echo("You are not the host of the listing from this booking id.")
        return
    
    sql_query = "INSERT INTO UserReviews (commentedOn, commentedBy, comment, rating) VALUES (%s, %s, %s, %s)"

    comment = click.prompt("Please enter a comment about the user., type=str, default="", show_default=False")
    if comment == "":
        comment = None
    rating = click.prompt("Please enter a rating from 1 to 5",type=int,default=None, show_default=False)
    if rating == "":
        rating = None
    elif rating < 1 or rating > 5:
        click.echo("Invalid rating.")
        return
    db_cursor.execute(sql_query, (renterSin, host_sin, comment, rating))
    db_connection.commit()
    db_cursor.close()
    click.echo("Thank you for your rating and comment.")

@click.pass_context
def rate(ctx,bookingid):
    sin = ctx.obj["userSIN"]
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()
    checkListing_query = "SELECT * FROM BookedBy WHERE bookingId = %s AND renterSIN = %s"
    db_cursor.execute(checkListing_query, (bookingid, sin))
    result = db_cursor.fetchone()
    if result is None:
        click.echo("Not a valid bookingId, or you are not the renter of this booking.")
        return
    if result[5] ==1:
        click.echo("You have cancelled this booking.")
        return
    listingid = result[1]
    checkRating_query = "SELECT * FROM ListingReviewAndComments WHERE listingId = %s AND renterSIN = %s"
    db_cursor.execute(checkRating_query, (listingid,sin))
    result = db_cursor.fetchone()
    if result is not None:
        click.echo("You have already rated or commented on this listing.")
        return
    rating = click.prompt("Please enter a rating from 1 to 5",type=int,default=None, show_default=False)
    if rating == "":
        rating = None
    elif rating < 1 or rating > 5:
        click.echo("Invalid rating.")
        return
    comment = click.prompt("Please enter a comment about the listing.", type=str, default="", show_default=False)
    if comment == "":
        comment = None
    addRating_query = "INSERT INTO ListingReviewAndComments (listingId, renterSIN, rating, comment) VALUES (%s, %s, %s, %s)"
    db_cursor.execute(addRating_query, (listingid,sin,rating,comment))
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    click.echo("Thank you for your rating and comment.")
    return