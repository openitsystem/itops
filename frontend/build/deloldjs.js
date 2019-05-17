let fs = require('fs');
function FileListPlugin(options) {}
FileListPlugin.prototype.apply = function(compiler) {
  compiler.plugin("done", function (stats) {
    var jsfilenamelist = Object.getOwnPropertyNames(stats.compilation.assets)
    for (var i = 0; i < jsfilenamelist.length ; i++) {
      if (jsfilenamelist[i].indexOf('.js.gz') !== -1 && jsfilenamelist[i].indexOf('static/js/') !== -1) {
        fs.writeFileSync('./dist/' + jsfilenamelist[i].replace(/.gz/g,''), ' ')
      }
    }
  });
}
module.exports = FileListPlugin;