function padzeros(number, length) {
    var num = '' + number;
    while (num.length < length) {
        num = '0' + num;
    }
    return num;
}

function startNumbersAt(num) {
    alert(num);
}

//var toggles = document.getElementsByClassName("dropdown-toggle");
//var i;
//for (i = 0; i < toggles.length; i++) {
//    var contents = toggles[i].parentElement.getElementsByClassName("dropdown-contents")[0];
//    toggles[i].contents = contents;
//    contents.onmouseover = function() {
//        this.contents.ismouseover = true;
//    }
//    toggles[i].onmouseover = function(event) {
//        this.ismouseover = true;
//        this.contents.style.display = "block";
//        
//    };
//    contents.onmouseout = function() {
//        this.contents.ismouseover = false;
//        if (!this.ismouseover) {
//            this.contents.style.display = "none";
//        }
//    };
//    toggles[i].onmouseout = function(mouseevent) {
//        this.ismouseover = false;
//        alert(this.contents.ismouseover);
//        if (!this.contents.ismouseover) {
//            this.contents.style.display = "none";
//        }
//    };
//}
