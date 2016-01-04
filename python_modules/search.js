function zip(arrays) {
    return arrays[0].map(function(_,i){
        return arrays.map(function(array){return array[i]})
    });
}

function levenshtein(s, len_s, t, len_t):
    var cost = 0;
    if (len_s == 0) {
        return len_t;
    }
    if (len_t == 0) {
        return len_s;
    }
    if (s[len_s-1] == t[len_t-1]) {
        cost = 0;
    }
    else {
        cost = 1;
    }
    return min(levenshtein(s, len_s - 1, t, len_t) + 1, levenshtein(s, len_s, t, len_t - 1) + 1, levenshtein(s, len_s - 1, t, len_t - 1) + cost);

function searchSort(query, nameList) {
	var names = query.lower().split(' ');
    var first = names[0];
    var last = names[1];
    var arr = [];
    for (var e in nameList) {
    	var n = e.lower().split(' ');
    	var f = n[0];
    	var l = n[1];
    	arr.push(levenshtein(first,first.length,f,f.length) + levenshtein(last,last.length,l,l.length));
    }
    arr = zip(nameList, arr);


}