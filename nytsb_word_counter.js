function get_sb_words(){
   let wa = [];
   for (const spn of document.getElementsByTagName("span")) {
      if (spn.className == "sb-anagram") {
         let word = spn.innerHTML.replace("<span class=\"sb-anagram-key\">", "").replace("</span>", "");
         if (wa.includes(word)){
            break;
         }
         wa.push(word);
      }
   }
   return wa;
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
         if (wl_set.includes(wl)) {
            continue;
         }
         wl_set.push(wl);
      }
   }
   let grid = " ";
   for (const wl of wl_set){
      grid += " " + wl;
   }
   grid += " Tot\n"
   for (const [w0, wlc] of Object.entries(word_count)){
      grid += w0;
      subtot = 0
      for (const wl of wl_set){
         if (wl in wlc) {
            grid += " " + wlc[wl];
            subtot += wlc[wl];
         } else {
            grid += " -";
         }
      }
      grid += " " + subtot + "\n";
   }
   return grid;
}

grid = make_grid(count_words(get_sb_words()));
console.log(grid);
