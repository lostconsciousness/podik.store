const xml2js = require('xml2js');
const fs = require('fs');
const {DOMParser} = require('xmldom');

let allDone = "";

fs.readFile(__dirname+'/offer.xml', "UTF-8", function(err,data){
    if(err) throw new Error(err);
    const parser = new xml2js.Parser();
    const xmlStringSerialized = new DOMParser().parseFromString(data, "text/xml");

    parser.parseString(xmlStringSerialized, function(err,res){
        if(err) return console.log(err);
        else{
            allDone = JSON.stringify(res,null,1);
            // fs.writeFile(__dirname+'/podiki.json', allDone, (e)=>{
            //     if(e) return console.log(e);
            //     return console.log("success");
            // })
            
            console.log(res.yml_catalog.shop[0].offers[0].offer[0].param);
        }
    })

});
