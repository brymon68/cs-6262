/**Frame bust code - after much trouble (trying to use document.write to write to dom),
I found: http://stackoverflow.com/questions/19941866/document-write-overwriting-the-document
which states that document.write wont overwrite if it is run at before document has loaded. This created timing issue
Therefore, following other examples of SO, I found document.createElement which is called immidiately **/
var node = document.createElement("script");
node.textContent = "if (top != self) \
 {window.self = window.top}"
document.documentElement.appendChild(node);
