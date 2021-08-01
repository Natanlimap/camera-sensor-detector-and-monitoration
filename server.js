const shell = require('shelljs')

var express = require('express');
var app = express();
const port = 3000

// respond with "hello world" when a GET request is made to the homepage
app.get('/:video', function(req, res) {
    console.log("Server delete")
    res.send(req.params.video);
    shell.exec("python3 controller.py 9")
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)

})