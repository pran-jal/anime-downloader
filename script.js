fs = require('fs');

fs.readFile('d.HTML', 'utf8', function (err,data) {
  if (err) {
    return console.log(err);
  }
  console.log(document.getElementById("main-wrapper").innerHTML );
});