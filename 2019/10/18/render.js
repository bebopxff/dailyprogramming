
self.importScripts('https://cdn.bootcss.com/showdown/1.9.0/showdown.min.js')

const convert = (text) => {
    let converter = new showdown.Converter()
    converter.setFlavor('github')
    return converter.makeHtml(text)
}

onmessage = function (e) {
  console.log('Message received from main script');
  // var workerResult = 'Result: ' + (e.data[0] * e.data[1]);
  console.log('Posting message back to main script');
  postMessage(convert(e.data));
}