This Flask-powered microblog has three methods:

* **write_post(title, text)**: will create a new post based on the title and text supplied.
* **read_posts()**: will return a list of the post objects in the database, with the most recently created posts first.
* **read_post(id)**: will return the post identified by id or raise an appropriate error if none is found.

I use [Bootstrap](http://getbootstrap) and the [Superhero](http://bootswatch.com/superhero/) Bootstrap theme created by [Thomas Park](https://github.com/thomaspark/bootswatch) to make the site look as nice as it does; any visual car wrecks are my own fault.