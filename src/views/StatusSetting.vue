<template>
    <div style="min-height: 100vh;" class="content">
        <div style="position: relative;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{ $t(`StatusSetting`) }}</h1>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <h3 class="box1h3text" style="color:#c2bfbf;margin:10px">{{ $t(`StatusSettingSection2`) }}</h3>
                <div style="text-align: right;padding-right:10px">
                    <input type="file" id="fileInput" style="visibility:hidden;width: 10px" @change="loadFileUpload()">
                    <button class="button-6" role="button" @click="openFileUpload()">{{ $t(`Import Setting`) }}</button>
                    <button class="button-6" role="button" @click="download()">{{ $t(`Export Setting`) }}</button>
                    <button class="button-6" role="button" style="background-color:rgb(211, 55, 16);color:#fff"
                        @click="resetprogress()">{{ $t(`Reset`) }}</button>
                </div>
                <div v-for="(ID_id, ID_index) in All_IDs" :key="ID_index">
                    <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                    <h2 class="box1h2text">{{ $t(ID_to_name(ID_index)) }}</h2>
                    <h3 class="box1h3text" style="text-align: left;">{{ $t(`Identities`) }}</h3>
                    <li style="text-align: left;padding-left:10vw;" v-for="(id, index) in ID_id.IDs" :key="index">
                        {{ id.rarity }}&nbsp;{{ $t(index) }}
                        &nbsp;
                        <div>
                            <select :id='ID_index + index' :v-model="ID_id.IDs"
                                @change="id.uptied = getitemselected(ID_index + index), updateIDdata()">
                                <option value=0>{{ $t(`Don't have`) }}</option>
                                <option value=1>{{ $t(`Uptie`) }}1</option>
                                <option value=2>{{ $t(`Uptie`) }}2</option>
                                <option value=3>{{ $t(`Uptie`) }}3</option>
                                <option value=4>{{ $t(`Uptie`) }}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                    <h3 class="box1h3text" style="text-align: left;">EGO</h3>
                    <li style="text-align: left;padding-left:10vw;" v-for="(id, index) in ID_id.EGOs" :key="index">
                        {{ id.rarity }}&nbsp;{{ $t(index) }}
                        &nbsp;
                        <div>
                            <select :id='ID_index + index' :v-model="ID_id.EGOs"
                                @change="id.uptied = getitemselected(ID_index + index), updateIDdata()">
                                <option value=0>{{ $t(`Don't have`) }}</option>
                                <option value=1>{{ $t(`Uptie`) }}1</option>
                                <option value=2>{{ $t(`Uptie`) }}2</option>
                                <option value=3>{{ $t(`Uptie`) }}3</option>
                                <option value=4>{{ $t(`Uptie`) }}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </div>
                <!-- <button @click="getcurrentiddata()">Submit</button> -->
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'StatusSetting',
    props: ['StatusData'],
    data() {
        return {
            All_IDs: {
                YiSangIDs: {
                    IDs: {
                        "Effloresced E.G.O::Spicebush YiSang": { rarity: "000", uptied: "0" },
                        "Blade Lineage Salsu YiSang": { rarity: "000", uptied: "0" },
                        "W Corp. L3 Cleanup Agent YiSang": { rarity: "000", uptied: "0" },
                        "Seven Assoc. South Section 6 YiSang": { rarity: "00", uptied: "0" },
                        "Molar Office Fixer YiSang": { rarity: "00", uptied: "0" },
                        "LCB Sinner YiSang": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "Crow's Eye View": { rarity: "Z", uptied: "0" },
                        "4th Match Flame": { rarity: "T", uptied: "0" },
                        "Wishing Cairn": { rarity: "T", uptied: "0" },
                        "Dimension Shredder": { rarity: "H", uptied: "0" },
                        "Sunshower": { rarity: "H", uptied: "0" }
                    },
                },
                FaustIDs: {
                    IDs: {
                        "Seven Assoc. South Section 4 Faust": { rarity: "000", uptied: "0" },
                        "The One Who Grips Faust": { rarity: "000", uptied: "0" },
                        "Lobotomy E.G.O::Regret Faust": { rarity: "000", uptied: "0" },
                        "Lobotomy Corp Remnant Faust": { rarity: "00", uptied: "0" },
                        "W Corp. L2 Cleanup Agent Faust": { rarity: "00", uptied: "0" },
                        "Zwei Assoc. South Section 4 Faust": { rarity: "00", uptied: "0" },
                        "LCB Sinner Faust": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "Representation Emitter": { rarity: "Z", uptied: "0" },
                        "Hex Nail": { rarity: "T", uptied: "0" },
                        "9:2": { rarity: "T", uptied: "0" },
                        "Telepole": { rarity: "H", uptied: "0" },
                        "Fluid Sac": { rarity: "H", uptied: "0" },
                    },
                },
                DonIDs: {
                    IDs: {
                        "Cinq Assoc. South Section 5 Director Don Quixote": { rarity: "000", uptied: "0" },
                        "W Corp. L3 Cleanup Agent Don Quixote": { rarity: "000", uptied: "0" },
                        "The Middle Little Sister Don Quixote": { rarity: "000", uptied: "0" },
                        "Shi Assoc. South Section 5 Director Don Quixote": { rarity: "00", uptied: "0" },
                        "N Corp. Mittelhammer Don Quixote": { rarity: "00", uptied: "0" },
                        "LCB Sinner Don Quixote": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "La Sangre de Sancho": { rarity: "Z", uptied: "0" },
                        "Lifetime Stew": { rarity: "T", uptied: "0" },
                        "Fluid Sac": { rarity: "H", uptied: "0" },
                        "Telepole": { rarity: "H", uptied: "0" },
                    },
                },
                RyoshuIDs: {
                    IDs: {
                        "W Corp. L3 Cleanup Agent Ryoshu": { rarity: "000", uptied: "0" },
                        "R.B. Chef de Cuisine Ryoshu": { rarity: "000", uptied: "0" },
                        "Kurokumo Clan Wakashu Ryoshu": { rarity: "000", uptied: "0" },
                        "Seven Assoc. South Section 6 Ryoshu": { rarity: "00", uptied: "0" },
                        "LCCB Assistant Manager Ryoshu": { rarity: "00", uptied: "0" },
                        "LCB Sinner Ryoshu": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "Forest for the Flames": { rarity: "Z", uptied: "0" },
                        "Soda": { rarity: "Z", uptied: "0" },
                        "Red Eyes": { rarity: "T", uptied: "0" },
                        "Blind Obsession": { rarity: "T", uptied: "0" },
                        "4th Match Flame": { rarity: "H", uptied: "0" },
                        "Red Eyes (Open)": { rarity: "H", uptied: "0" },
                    },
                },
                MeurIDs: {
                    IDs: {
                        "R Corp. 4th Pack Rhino Meursault": { rarity: "000", uptied: "0" },
                        "N Corp. GroBHammer Meursault": { rarity: "000", uptied: "0" },
                        "W Corp. L2 Cleanup Agent Meursault": { rarity: "000", uptied: "0" },
                        "Liu Assoc. South Section 6 Meursault": { rarity: "00", uptied: "0" },
                        "The Middle Little Brother Meursault": { rarity: "00", uptied: "0" },
                        "Rosespanner Workshop Fixer Meursault": { rarity: "00", uptied: "0" },
                        "LCB Sinner Meursault": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "Chains of Others": { rarity: "Z", uptied: "0" },
                        "Screwloose Wallop": { rarity: "T", uptied: "0" },
                        "Regret": { rarity: "T", uptied: "0" },
                        "Capote": { rarity: "H", uptied: "0" },
                        "Pursuance": { rarity: "H", uptied: "0" },
                    },
                },
                HongLuIDs: {
                    IDs: {
                        "Ting Tang Gang Gangleader Hong Lu": { rarity: "000", uptied: "0" },
                        "K Corp. Class 3 Excision Staff Hong Lu": { rarity: "000", uptied: "0" },
                        "Kurokumo Clan Wakashu Hong Lu": { rarity: "00", uptied: "0" },
                        "W Corp. L2 Cleanup Agent Hong Lu": { rarity: "00", uptied: "0" },
                        "Liu Assoc. South Section 5 Hong Lu": { rarity: "00", uptied: "0" },
                        "Hook Office Fixer Hong Lu": { rarity: "00", uptied: "0" },
                        "LCB Sinner Hong Lu": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "Land of Illusion": { rarity: "Z", uptied: "0" },
                        "Roseate Desire": { rarity: "T", uptied: "0" },
                        "Soda": { rarity: "T", uptied: "0" },
                        "Dimension Shredder": { rarity: "H", uptied: "0" },
                        "Effervescent Corrosion": { rarity: "H", uptied: "0" },
                    },
                },
                HeathIDs: {
                    IDs: {
                        "R Corp. 4th Pack Rabbit Heathcliff": { rarity: "000", uptied: "0" },
                        "Lobotomy E.G.O::Sunshower Heathcliff": { rarity: "000", uptied: "0" },
                        "Shi Assoc. South Section 5 Heathcliff": { rarity: "00", uptied: "0" },
                        "Seven Assoc. South Section 4 Heathcliff": { rarity: "00", uptied: "0" },
                        "N Corp. Kleinhammer Heathcliff": { rarity: "00", uptied: "0" },
                        "LCB Sinner Heathcliff": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "Bodysack": { rarity: "Z", uptied: "0" },
                        "AEDD": { rarity: "T", uptied: "0" },
                        "Ya Sunyata Tad Rupam": { rarity: "H", uptied: "0" },
                        "Telepole": { rarity: "H", uptied: "0" },
                    },
                },
                IshIDs: {
                    IDs: {
                        "Molar Boatworks Fixer Ishmael": { rarity: "000", uptied: "0" },
                        "R Corp. 4th Pack Reindeer Ishmael": { rarity: "000", uptied: "0" },
                        "Liu Assoc. South Section 4 Ishmael": { rarity: "000", uptied: "0" },
                        "Lobotomy E.G.O::Sloshing Ishmael": { rarity: "00", uptied: "0" },
                        "Shi Assoc. South Section 5 Ishmael": { rarity: "00", uptied: "0" },
                        "LCCB Assistant Manager Ishmael": { rarity: "00", uptied: "0" },
                        "LCB Sinner Ishmael": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "Snagharpoon": { rarity: "Z", uptied: "0" },
                        "Roseate Desire": { rarity: "T", uptied: "0" },
                        "Capote": { rarity: "T", uptied: "0" },
                        "Ardor Blossom Star": { rarity: "H", uptied: "0" },
                        "Blind Obsession": { rarity: "W", uptied: "0" },
                    },
                },
                RodionIDs: {
                    IDs: {
                        "Kurokumo Clan Wakashu Rodion": { rarity: "000", uptied: "0" },
                        "Rosespanner Workshop Rep Rodion": { rarity: "000", uptied: "0" },
                        "Dieci Assoc. South Section 4 Rodion": { rarity: "000", uptied: "0" },
                        "LCCB Assistant Manager Rodion": { rarity: "00", uptied: "0" },
                        "Zwei Assoc. South Section 5 Rodion": { rarity: "00", uptied: "0" },
                        "N Corp. Mittelhammer Rodion": { rarity: "00", uptied: "0" },
                        "LCB Sinner Rodion": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "What is Cast": { rarity: "Z", uptied: "0" },
                        "Rime Shank": { rarity: "T", uptied: "0" },
                        "Effervescent Corrosion": { rarity: "T", uptied: "0" },
                        "4th Match Flame": { rarity: "H", uptied: "0" },
                    },
                },
                SinclairIDs: {
                    IDs: {
                        "Blade Lineage Salsu Sinclair": { rarity: "000", uptied: "0" },
                        "The One Who Shall Grip Sinclair": { rarity: "000", uptied: "0" },
                        "Zwei Assoc. South Section 6 Sinclair": { rarity: "00", uptied: "0" },
                        "Los Mariachis Jefe Sinclair": { rarity: "00", uptied: "0" },
                        "Lobotomy E.G.O::Red Sheet Sinclair": { rarity: "00", uptied: "0" },
                        "Molar Boatworks Fixer Sinclair": { rarity: "00", uptied: "0" },
                        "LCB Sinner Sinclair": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "Branch of Knowledge": { rarity: "Z", uptied: "0" },
                        "Impending Day": { rarity: "T", uptied: "0" },
                        "Lifetime Stew": { rarity: "T", uptied: "0" },
                        "Lantern": { rarity: "H", uptied: "0" },
                        "9:2": { rarity: "H", uptied: "0" },
                    },
                },
                OutisIDs: {
                    IDs: {
                        "Seven Assoc. South Section 6 Director Outis": { rarity: "000", uptied: "0" },
                        "Molar Office Fixer Outis": { rarity: "000", uptied: "0" },
                        "G Corp. Head Manager Outis": { rarity: "00", uptied: "0" },
                        "Blade Lineage Cutthroat Outis": { rarity: "00", uptied: "0" },
                        "LCB Sinner Outis": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "To pathos Mathos": { rarity: "Z", uptied: "0" },
                        "Sunshower": { rarity: "T", uptied: "0" },
                        "Ya Sunyata Tad Rupam": { rarity: "T", uptied: "0" },
                        "Ebony Stem": { rarity: "H", uptied: "0" },
                    },
                },
                GregorIDs: {
                    IDs: {
                        "G Corp. Manager Corporal Gregor": { rarity: "000", uptied: "0" },
                        "Twinhook Pirates First Mate Gregor": { rarity: "000", uptied: "0" },
                        "Zwei Assoc. South Section 4 Gregor": { rarity: "000", uptied: "0" },
                        "Rosespanner Workshop Fixer Gregor": { rarity: "00", uptied: "0" },
                        "Liu Assoc. South Section 6 Gregor": { rarity: "00", uptied: "0" },
                        "R.B. Sous-chef Gregor": { rarity: "00", uptied: "0" },
                        "LCB Sinner Gregor": { rarity: "0", uptied: "0" },
                    },
                    EGOs: {
                        "Suddenly,One Day": { rarity: "Z", uptied: "0" },
                        "Legerdemain": { rarity: "Z", uptied: "0" },
                        "AEDD": { rarity: "T", uptied: "0" },
                        "Lantern": { rarity: "H", uptied: "0" },
                    },
                },
            }
        }
    },
    computed: {
    },
    methods: {
        //for debugging
        testing() {
            console.log(this.$data);
        },
        ID_to_name(itemID) {
            var CorrName;
            switch (itemID) {
                case "YiSangIDs":
                    CorrName = "YiSang";
                    break;
                case "FaustIDs":
                    CorrName = "Faust";
                    break;
                case "DonIDs":
                    CorrName = "Don Quixote";
                    break;
                case "RyoshuIDs":
                    CorrName = "Ryoshu";
                    break;
                case "MeurIDs":
                    CorrName = "Meursault";
                    break;
                case "HongLuIDs":
                    CorrName = "Hong Lu";
                    break;
                case "HeathIDs":
                    CorrName = "Heathcliff";
                    break;
                case "IshIDs":
                    CorrName = "Ishmael";
                    break;
                case "RodionIDs":
                    CorrName = "Rodion";
                    break;
                case "SinclairIDs":
                    CorrName = "Sinclair";
                    break;
                case "OutisIDs":
                    CorrName = "Outis";
                    break;
                case "GregorIDs":
                    CorrName = "Gregor";
                    break;
            }
            return CorrName;
        },
        testinglog(item) {
            console.log(item);
        },
        //update the data to local storage
        updateIDdata() {
            localStorage.setItem('IDdata', JSON.stringify(this.All_IDs));
        },
        //for getting the option value
        getitemselected(item) {
            var e = document.getElementById(item);
            return e.value;
        },
        download() {
            var type = "text/plain";
            var text = JSON.stringify(this.All_IDs);
            var filename = "StatusSetting.txt";
            // Create an invisible A element
            const a = document.createElement("a");
            a.style.display = "none";
            document.body.appendChild(a);
            // Set the HREF to a Blob representation of the data to be downloaded
            a.href = window.URL.createObjectURL(
                new Blob([text], { type })
            );
            // Use download attribute to set set desired file name
            a.setAttribute("download", filename);
            // Trigger the download by simulating click
            a.click();
            // Cleanup
            window.URL.revokeObjectURL(a.href);
            document.body.removeChild(a);
        },
        openFileUpload() { //click the hidden file input button
            document.getElementById("fileInput").click();
        },
        loadFileUpload() {
            var fileInput = document.getElementById('fileInput');
            var file = fileInput.files[0];
            var textType = /text.*/;

            if (file.type.match(textType)) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    var content = reader.result;
                    //Here the content has been read successfuly
                    localStorage.setItem('IDdata', content);
                    // console.log(content);
                }
                reader.readAsText(file);
                location.reload();
            }
        },
        //restore the progress, used in the mounted()
        restoreprogress() {
            var restoredata = JSON.parse(localStorage.getItem('IDdata'));
            if (restoredata) {

                //for checking if there is newly added data(aka game updated new stuff)
                for (const [key1, value1] of Object.entries(this.All_IDs)) {
                    //key = YiSangIDs...  value1 = IDs, EGOs
                    if (!restoredata[key1]) {
                        console.log(key1);
                    }
                    for (const [key2, value2] of Object.entries(this.All_IDs[key1].IDs)) {
                        //key2 = Effloresced E.G.O::Spicebush YiSang...  value2 = rarity, uptied

                        //if something not in the restoredata, add it
                        if (!restoredata[key1].IDs[key2]) {
                            console.log(key1 + " IDs " + key2);
                            restoredata[key1].IDs[key2] = this.All_IDs[key1].IDs[key2];
                            localStorage.setItem('IDdata', JSON.stringify(restoredata));
                        }
                    }
                    for (const [key3, value2] of Object.entries(this.All_IDs[key1].EGOs)) {
                        if (!restoredata[key1].EGOs[key3]) {
                            console.log(key1 + " EGOs " + key3);
                            restoredata[key1].EGOs[key3] = this.All_IDs[key1].EGOs[key3];
                            localStorage.setItem('IDdata', JSON.stringify(restoredata));
                        }
                    }
                }
                this.All_IDs = restoredata;
                var restoreid;
                for (const [key, value] of Object.entries(this.All_IDs)) {
                    restoreid = key;
                    for (const [key2, value2] of Object.entries(value.IDs)) {
                        document.getElementById(restoreid + key2).value = value2.uptied;
                    }
                    for (const [key3, value3] of Object.entries(value.EGOs)) {
                        document.getElementById(restoreid + key3).value = value3.uptied;
                    }
                }
            } else {
                localStorage.setItem('IDdata', JSON.stringify(this.All_IDs));
            }
        },

        //remove the localstorage data + reset everything
        resetprogress() {
            localStorage.removeItem('IDdata');
            for (const [key1, value1] of Object.entries(this.All_IDs)) {
                var selectvalue = value1;
                var selectkey = key1;
                for (const [key2, value2] of Object.entries(selectvalue.IDs)) {
                    // console.log(selectkey+key2);
                    document.getElementById(selectkey + key2).value = 0;
                    value2.uptied = 0;
                }
                for (const [key2, value2] of Object.entries(selectvalue.EGOs)) {
                    // console.log(selectkey+key2);
                    document.getElementById(selectkey + key2).value = 0;
                    value2.uptied = 0;
                }
            }
            localStorage.setItem('IDdata', JSON.stringify(this.All_IDs));
        }
    },
    created() {
        // console.log(this.$data);
    },
    mounted() {
        //call restoreprogress funct when DOMContentLoaded
        document.addEventListener('DOMContentLoaded', this.restoreprogress);

        //reload the page for addeventlistener rlly show result
        if (localStorage.getItem('reloaded')) { //just reloaded
            localStorage.removeItem('reloaded');
        } else {
            // Set a flag so that we know not to reload the page twice.
            localStorage.setItem('reloaded', '1');
            location.reload();
        }
    },
}
</script>

<style>
select {
    appearance: none;
    /* safari */
    -webkit-appearance: none;
    /* other styles for aesthetics */
    width: auto;
    min-width: 15vw;
    font-size: 1rem;
    padding: 0.675em 1em 0.675em 1em;
    background-color: #fff;
    border: 1px solid #caced1;
    border-radius: 0.25rem;
    color: #000;
    cursor: pointer;
}

/* CSS */
.button-6 {
    align-items: center;
    background-color: #fff;
    border: 1px solid rgba(255, 59, 59, 0.1);
    border-radius: .25rem;
    box-shadow: rgba(0, 0, 0, 0.02) 0 1px 3px 0;
    box-sizing: border-box;
    color: rgba(0, 0, 0, 0.85);
    cursor: pointer;
    display: inline-flex;
    font-family: system-ui, -apple-system, system-ui, "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 15px;
    font-weight: 500;
    justify-content: center;
    line-height: 1.25;
    margin: 0;
    min-height: 3rem;
    padding: calc(.775rem - 1px) calc(1.2rem - 1px);
    position: relative;
    text-decoration: none;
    transition: all 250ms;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: baseline;
    width: auto;
}

.button-6:hover,
.button-6:focus {
    border-color: rgba(0, 0, 0, 0.15);
    box-shadow: rgba(0, 0, 0, 0.1) 0 4px 12px;
    color: rgba(0, 0, 0, 0.65);
}

.button-6:hover {
    transform: translateY(-1px);
}

.button-6:active {
    background-color: #F0F0F1;
    border-color: rgba(0, 0, 0, 0.15);
    box-shadow: rgba(0, 0, 0, 0.06) 0 2px 4px;
    color: rgba(0, 0, 0, 0.65);
    transform: translateY(0);
}
</style>
  

  