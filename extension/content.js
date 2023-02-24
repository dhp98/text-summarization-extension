console.log("Text Summarizer working..")

const texts = document.getElementsByTagName('p');
let text_to_summarize = "";

for (elt of texts){
    // console.log(elt.textContent);
    text_to_summarize += elt.textContent;
}

console.log(text_to_summarize);

fetch("http://127.0.0.1:3000/summarize", {
    method: "POST",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({"data": text_to_summarize})
})
.then(response => response.json())
.then((response)=>{
    console.log(JSON.stringify(response));

    let output = "\nSummary of web page is: \n";
    for (elt of response['data']){
        output +="\u2022"+elt +"\n";
    }

    alert(output);
});