function populate(s1,s2){
    var s1 = document.getElementById(s1);
    var s2 = document.getElementById(s2);
    s2.innerHTML = "";
    if(s1.value == "Brazil"){
        var optionArray = ["", "Flamengo", "Palmeiras", "Cruzeiro"];
    }
    if(s1.value == "International"){
        var optionArray = ["", "Barcelona", "Bayern", "Real Madrid"];
    }
    if(s1.value == "novice"){
        var optionArray = ["0","1","2","3","4","5","6","7","8","9","10"];
    }
    if(s1.value == "super_novice"){
        var optionArray = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99"];
    }
//    if(s1.value == "swordsman" || s1.value == "mage"){
    var first_job = ["swordsman", "mage", "archer", "acolyte", "merchant", "thief", "taekwon", "star_gladiator", "soul_linker", "gunslinger", "ninja"]
    if(first_job.indexOf(s1.value) > -1){
        var optionArray = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"];
    }

    var second_job = ["knight", "priest", "wizard", "blacksmith", "hunter", "assassin", "crusader", "rogue", "sage", "alchemist", "monk", "bard", "dancer"]
    if(second_job.indexOf(s1.value) > -1){
        var optionArray = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"];
    }

    var trans_job = ["lord_knight", "hihg_priest", "high_wizard", "whitesmith", "sniper", "assassin_cross", "paladin", "stalker", "professor", "creator", "champion", "clown", "gypsy"]
    if(trans_job.indexOf(s1.value) > -1){
        var optionArray = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70"]
    }

    for(var option in optionArray){
        var pair = optionArray[option];
        var newOption = document.createElement("option");
        newOption.value = pair;
        newOption.innerHTML = pair;
        s2.options.add(newOption);
        }
}

function default_job_level(s1){
    console.log("oi")
}