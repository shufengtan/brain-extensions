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
   }
   return word_count
}

function diff_shunns_grid(word_count){
   const shunns_word_count = {}; // This needs to be provided
   let diff = "";
   for (const [w0, wlc] of Object.entries(shunns_word_count)){
      w0lc = w0.toLowerCase()
      for (const [wl, c] of Object.entries(wlc)){
         let c1 = 0;
         if (w0lc in word_count && wl in word_count[w0lc]){
            c1 = word_count[w0lc][wl];
         }
         diff += " " + w0 + wl + ": "  + c1 + "/" + c + ", ";
      }
      diff += "
";
   }
   return diff;
}

(function() {
//   console.log(get_sb_grid());
   let diff = diff_shunns_grid(count_words(get_sb_words()));
   //alert(diff);
   console.log(diff);
   //alert(get_sb_grid());
})();
