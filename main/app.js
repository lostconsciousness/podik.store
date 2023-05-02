let tg = window.Telegram.WebApp;
tg.expand()
tg.MainButton.textColor = "#FFFFFF";
tg.MainButton.color = "#2cab37";

let item = "";

let btn = document.getElementsByClassName("button_card")


btn.addEventListener("click", function(){
    if(tg.MainButton.isVisible){
        tg.MainButton.hide();
    }
    else{
        tg.MainButton.setText("sosi");
        item = "1";
        tg.MainButton.show();
    }
});

Telegram.Webapp.onEvent("mainButtonClicked", function (){
    tg.setData(item);
});

