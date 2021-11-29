// Please read Dan Harper's gist https://gist.github.com/danharper/8364399
// to install this as a Chrome extension

function get_sb_words(){
   let wlist = [];
   const tag_re = /<[^>]+>/g;
   for (const spn of document.getElementsByTagName("span")) {
      if (spn.className == "sb-anagram") {
         let word = spn.innerHTML.replace(tag_re, "");
         if (wlist.includes(word)) break;
         wlist.push(word);
      }
   }
   return wlist;
}

function count_words(word_list){
   let word_count = {};
   for (const word of word_list) {
      let w0 = word[0];
      let wl = word.length;
      if (w0 in word_count){
         if (wl in word_count[w0]) {
            word_count[w0][wl]++;
        } else {
            word_count[w0][wl] = 1;
        }
     } else {
        word_count[w0] = {};
        word_count[w0][wl] = 1;
     }
     let tc = w0 + word[1];
     if (tc in word_count) {
         word_count[tc]++;
     } else {
         word_count[tc] = 1;
     }
   }
   return word_count
}

function async_get_http(url, callback){
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
}

function remove_html_tags(text){
    text = text.substring(text.indexOf("Spelling Bee Grid"));
    text = text.substr(0, text.indexOf('<h2 class="css-'));
    text = text.replaceAll(/<(br\/|p\b[^>]*)>/g, "\n");
    text = text.replaceAll(/<[^>]+>/g, "");
    return text;
}

function parse_hints_text(text){
    text = remove_html_tags(text).replaceAll(/\t/g, "");
    let wlen;
    let hints_word_count = {};
    for (const line of text.split("\n")) {
        if (/^[ \d]+Σ$/.test(line)){
            wlen = line.replace(/^ +/, "").replace(/ *Σ/, "").replaceAll(/ +/g, " ").split(" ");
        } else if (/^[A-Z]: /.test(line)) {
            c0 = line.substring(0, 1);
            hints_word_count[c0] = {}
            let w_counts = line.replace(/^[A-Z]: +/, "").replaceAll(/ +/g, " ").split(" ")
            for (let i = 0; i < w_counts.length - 1; i++) {
                if (w_counts[i] != '-') {
                    hints_word_count[c0][wlen[i]] = parseInt(w_counts[i]);
                }
            }
        } else if (/^[A-Z][A-Z]-\d/.test(line)) {
            for (const tlc of line.split(" ")) {
                let cc_c = tlc.split('-');
                hints_word_count[cc_c[0]] = parseInt(cc_c[1]);
            }
        }
    }
    // console.log(JSON.stringify(hints_word_count));
    let word_count = count_words(get_sb_words())
    // console.log(JSON.stringify(word_count));
    let diff = "";
    let diff2 = "";
    let prev_diff2 = "";
    let tot_delta = 0;
    for (const [w0, wlc] of Object.entries(hints_word_count)){
        let w0lc = w0.toLowerCase();
        if (w0.length == 2) {
            let tlc = 0;
            if (w0lc in word_count){ tlc = word_count[w0lc]; }
            if (w0lc[0] != prev_diff2){
                prev_diff2 = w0lc[0];
                diff2 += "\n";
            }
            diff2 += " " + w0 + "-" + tlc + "/" + wlc + ", ";
            continue;
        }
        let delta = 0;
        for (const [wl, c] of Object.entries(wlc)){
            let c1 = 0;
            if (w0lc in word_count && wl in word_count[w0lc]){
                c1 = word_count[w0lc][wl];
            }
            diff += " " + w0 + wl + ": "  + c1 + "/" + c + ", ";
            delta += c - c1;
        }
        diff += "("+delta + ")\n";
        tot_delta += delta;
    }
    if (tot_delta == 0){
        diff += "You have found them all!"
    } else {
        diff += tot_delta + " words to go."
    }
    console.log(diff + "\n" + diff2);
}

function diff_grid(){
   let today = (new Date()).toLocaleDateString()
   let hints_url = 'https://www.nytimes.com/' + today.substring(6, 10) + '/' + today.substring(0, 5) + '/crosswords/spelling-bee-forum.html';
   async_get_http(hints_url, parse_hints_text);
}

(function() {
   diff_grid();
})();
