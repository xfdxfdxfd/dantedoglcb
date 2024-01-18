<template>
    <div class="content">
        <div style="position: relative;">
            <div class="box box1">
                <h1 class="subtitle">{{ $t(`StatusSetting`) }}</h1>
                &nbsp;
                <h2 class="separator"></h2>
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
                    <h2 class="separator"></h2>
                    <h2 class="box1h2text">{{ $t(ID_to_name(ID_index)) }}</h2>
                    <h3 class="box1h3text" style="text-align: left;">{{ $t(`Identities`) }}</h3>
                    <div style="display:flex;flex-flow: row wrap;justify-content:flex-start">
                        <div style="text-align: left;padding-left:10vw;word-wrap: break-word;width:12vw;min-width:10px"
                            v-for="(id, index) in ID_id.IDs" :key="index">
                            {{ id.rarity.replace('Rarity', '') }}&nbsp;{{ $t(index) }}
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
                        </div>
                    </div>
                    <h3 class="box1h3text" style="text-align: left;">EGO</h3>
                    <div style="display:flex;flex-flow: row wrap;justify-content:flex-start">
                        <div style="text-align: left;padding-left:10vw;word-wrap: break-word;;width:12vw;min-width:10px"
                            v-for="(id, index) in ID_id.EGOs" :key="index">
                            {{ id.rarity.replace('notOriginal', '') }}&nbsp;{{ $t(index) }}
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
                        </div>
                    </div>
                </div>
                <!-- <button @click="getcurrentiddata()">Submit</button> -->
            </div>
        </div>
    </div>
</template>

<script>
import statusdata from '../components/data.js';
export default {
    name: 'StatusSetting',
    props: ['StatusData'],
    data() {
        return statusdata.data();
    },
    methods: {
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
        //for testing
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
                        //if the rarity is different, update it
                        if (restoredata[key1].IDs[key2].rarity != this.All_IDs[key1].IDs[key2].rarity) {
                            console.log(key1 + " IDs " + key2);
                            restoredata[key1].IDs[key2].rarity = this.All_IDs[key1].IDs[key2].rarity;
                            localStorage.setItem('IDdata', JSON.stringify(restoredata));
                        }
                    }
                    for (const [key3, value2] of Object.entries(this.All_IDs[key1].EGOs)) {
                        //if something not in the restoredata, add it
                        if (!restoredata[key1].EGOs[key3]) {
                            console.log(key1 + " EGOs " + key3);
                            restoredata[key1].EGOs[key3] = this.All_IDs[key1].EGOs[key3];
                            localStorage.setItem('IDdata', JSON.stringify(restoredata));
                        }
                        //if the rarity is different, update it
                        if (restoredata[key1].EGOs[key3].rarity != this.All_IDs[key1].EGOs[key3].rarity) {
                            console.log(key1 + " EGOs " + key3);
                            restoredata[key1].EGOs[key3].rarity = this.All_IDs[key1].EGOs[key3].rarity;
                            localStorage.setItem('IDdata', JSON.stringify(restoredata));
                        }
                    }
                }
                for (const [key, value] of Object.entries(this.All_IDs)) {
                    for (const [key2, value2] of Object.entries(value.IDs)) {
                        value2.uptied = restoredata[key].IDs[key2].uptied;
                        document.getElementById(key + key2).value = value2.uptied;
                    }
                    for (const [key3, value3] of Object.entries(value.EGOs)) {
                        value3.uptied = restoredata[key].EGOs[key3].uptied;
                        document.getElementById(key + key3).value = value3.uptied;
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
@import '../components/format.css';
</style>
  

  