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

function make_grid(word_count){
   let wl_set = [];
   for (const [w0, wlc] of Object.entries(word_count)){
      for (const [wl, c] of Object.entries(wlc)){
         if (! wl_set.includes(wl)) {
            wl_set.push(wl);
         }
      }
   }
   wl_set.sort();
   let grid = " ";
   for (const wl of wl_set){
      grid += " " + wl;
   }
   w0_list = Object.keys(word_count);
   w0_list.sort();
   grid += "  Tot\n"
   let total = 0;
   for (const w0 of w0_list){
      wlc = word_count[w0];
      grid += w0.toUpperCase();
      subtot = 0
      for (const wl of wl_set){
         if (wl in wlc) {
            grid += " " + wlc[wl];
            subtot += wlc[wl];
         } else {
            grid += " -";
         }
      }
      grid += "  [" + subtot + "]\n";
      total += subtot;
   }
   grid += "Tot " + total
   return grid;
}

function get_sb_grid(){
   return make_grid(count_words(get_sb_words()));
}
