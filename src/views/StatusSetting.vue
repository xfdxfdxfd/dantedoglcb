<template>
    <div style="min-height: 100vh;" class="content">
        <div style="position: relative;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{$t(`StatusSetting`)}}</h1>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <div>
                    <select id="IDs-select" style="width: 80%;background-color: rgb(255, 220, 161);" @change="getIDselected()">
                      <option value="YiSangIDs">{{$t(`YiSang`)}}</option>
                      <option value="FaustIDs">{{$t(`Faust`)}}</option>
                      <option value="DonIDs">{{$t(`Don Quixote`)}}</option>
                      <option value="RyoshuIDs">{{$t(`Ryoshu`)}}</option>
                      <option value="MeurIDs">{{$t(`Meursault`)}}</option>
                      <option value="HongLuIDs">{{$t(`Hong Lu`)}}</option>
                      <option value="HeathIDs">{{$t(`Heathcliff`)}}</option>
                      <option value="IshIDs">{{$t(`Ishmael`)}}</option>
                      <option value="RodionIDs">{{$t(`Rodion`)}}</option>
                      <option value="SinclairIDs">{{$t(`Sinclair`)}}</option>
                      <option value="OutisIDs">{{$t(`Outis`)}}</option>
                      <option value="GregorIDs">{{$t(`Gregor`)}}</option>
                    </select>
                </div>

                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(currentIDName)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in currentIDList.IDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentID+index' @change="id.uptied=getitemselected(currentID+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">EGO</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in currentIDList.EGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentID+index' @change="id.uptied=getitemselected(currentID+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>

                <button @click="testing()">Submit</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'StatusSetting',
  props: ['StatusData'],
  data(){
    return {
        currentselected:{id:"YiSangIDs",name:"YiSang"},
        YiSangIDs: {
            IDs: {
                "Effloresced E.G.O::Spicebush YiSang": {rarity:"000",owned:false, uptied:'0'},
                "Blade Lineage Salsu YiSang": {rarity:"000",owned:false, uptied:'0'},
                "W Corp. L3 Cleanup Agent YiSang": {rarity:"000",owned:false, uptied:'0'},
                "Seven Assoc. South Section 6 YiSang":{rarity:"00",owned:false,uptied:'0'},
                "Molar Office Fixer YiSang":{rarity:"00",owned:false,uptied:'0'},
                "LCB Sinner YiSang":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs:{
                "Crow's Eye View":{rarity:"Z",owned:false, uptied:'0'},
                "4th Match Flame":{rarity:"T",owned:false, uptied:'0'},
                "Wishing Cairn":{rarity:"T",owned:false, uptied:'0'},
                "Dimension Shredder":{rarity:"H",owned:false, uptied:'0'},
                "Sunshower":{rarity:"H",owned:false, uptied:'0'}
            },
        },
        FaustIDs: {
            IDs:{
                "Seven Assoc. South Section 4 Faust": {rarity:"000",owned:false, uptied:'0'},
                "The One Who Grips Faust": {rarity:"000",owned:false, uptied:'0'},
                "Lobotomy E.G.O::Regret Faust": {rarity:"000",owned:false, uptied:'0'},
                "Lobotomy Corp Remnant Faust": {rarity:"00",owned:false, uptied:'0'},
                "W Corp. L2 Cleanup Agent Faust": {rarity:"00",owned:false, uptied:'0'},
                "Zwei Assoc. South Section 4 Faust": {rarity:"00",owned:false, uptied:'0'},
                "LCB Sinner Faust":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs: {
                "Representation Emitter":{rarity:"Z",owned:false, uptied:'0'},
                "Hex Nail":{rarity:"T",owned:false, uptied:'0'},
                "Telepole":{rarity:"H",owned:false, uptied:'0'},
                "Fluid Sac":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        DonIDs: {
            IDs:{
                "Cinq Assoc. South Section 5 Director Don Quixote": {rarity:"000",owned:false, uptied:'0'},
                "W Corp. L3 Cleanup Agent Don Quixote": {rarity:"000",owned:false, uptied:'0'},
                "Shi Assoc. South Section 5 Director Don Quixote":{rarity:"00",owned:false,uptied:'0'},
                "N Corp. Mittelhammer Don Quixote":{rarity:"00",owned:false,uptied:'0'},
                "LCB Sinner Don Quixote":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs:{
                "La Sangre de Sancho":{rarity:"Z",owned:false, uptied:'0'},
                "Lifetime Stew":{rarity:"T",owned:false, uptied:'0'},
                "Fluid Sac":{rarity:"H",owned:false, uptied:'0'},
                "Telepole":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        RyoshuIDs: {
            IDs:{
                "W Corp. L3 Cleanup Agent Ryoshu": {rarity:"000",owned:false, uptied:'0'},
                "R.B. Chef de Cuisine Ryoshu": {rarity:"000",owned:false, uptied:'0'},
                "Kurokumo Clan Wakashu Ryoshu": {rarity:"000",owned:false, uptied:'0'},
                "Seven Assoc. South Section 6 Ryoshu": {rarity:"00",owned:false, uptied:'0'},
                "LCB Sinner Ryoshu":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs:{
                "Forest for the Flames":{rarity:"Z",owned:false, uptied:'0'},
                "Soda":{rarity:"Z",owned:false, uptied:'0'},
                "Red Eyes":{rarity:"T",owned:false, uptied:'0'},
                "4th Match Flame":{rarity:"H",owned:false, uptied:'0'},
                "Red Eyes (Open)":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        MeurIDs: {
            IDs: {
                "R Corp. 4th Pack Rhino Meursault": {rarity:"000",owned:false, uptied:'0'},
                "N Corp. GroBHammer Meursault": {rarity:"000",owned:false, uptied:'0'},
                "W Corp. L2 Cleanup Agent Meursault": {rarity:"000",owned:false, uptied:'0'},
                "Liu Assoc. South Section 6 Meursault": {rarity:"00",owned:false, uptied:'0'},
                "Rosespanner Workshop Fixer Meursault": {rarity:"00",owned:false, uptied:'0'},
                "LCB Sinner Meursault":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs:{
                "Chains of Others":{rarity:"Z",owned:false, uptied:'0'},
                "Screwloose Wallop":{rarity:"T",owned:false, uptied:'0'},
                "Regret":{rarity:"T",owned:false, uptied:'0'},
                "Capote":{rarity:"H",owned:false, uptied:'0'},
                "Pursuance":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        HongLuIDs: {
            IDs: {
                "Ting Tang Gang Gangleader Hong Lu": {rarity:"000",owned:false, uptied:'0'},
                "K Corp. Class 3 Excision Staff Hong Lu": {rarity:"000",owned:false, uptied:'0'},
                "Kurokumo Clan Wakashu Hong Lu": {rarity:"00",owned:false, uptied:'0'},
                "W Corp. L2 Cleanup Agent Hong Lu": {rarity:"00",owned:false, uptied:'0'},
                "Liu Assoc. South Section 5 Hong Lu": {rarity:"00",owned:false, uptied:'0'},
                "Hook Office Fixer Hong Lu": {rarity:"00",owned:false, uptied:'0'},
                "LCB Sinner Hong Lu":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs:{
                "Land of Illusion":{rarity:"Z",owned:false, uptied:'0'},
                "Roseate Desire":{rarity:"T",owned:false, uptied:'0'},
                "Soda":{rarity:"T",owned:false, uptied:'0'},
                "Dimension Shredder":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        HeathIDs: {
            IDs:{
                "R Corp. 4th Pack Rabbit Heathcliff": {rarity:"000",owned:false, uptied:'0'},
                "Lobotomy E.G.O::Sunshower Heathcliff": {rarity:"000",owned:false, uptied:'0'},
                "Shi Assoc. South Section 5 Heathcliff":{rarity:"00",owned:false,uptied:'0'},
                "Seven Assoc. South Section 4 Heathcliff":{rarity:"00",owned:false,uptied:'0'},
                "N Corp. Kleinhammer Heathcliff":{rarity:"00",owned:false,uptied:'0'},
                "LCB Sinner Heathcliff":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs:{
                "Bodysack":{rarity:"Z",owned:false, uptied:'0'},
                "AEDD":{rarity:"T",owned:false, uptied:'0'},
                "Ya Sunyata Tad Rupam":{rarity:"H",owned:false, uptied:'0'},
                "Telepole":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        IshIDs: {
            IDs:{
                "Molar Boatworks Fixer Ishmael":{rarity:"000",owned:false, uptied:'0'},
                "R Corp. 4th Pack Reindeer Ishmael":{rarity:"000",owned:false, uptied:'0'},
                "Liu Assoc. South Section 4 Ishmael":{rarity:"000",owned:false, uptied:'0'},
                "Lobotomy E.G.O::Sloshing Ishmael":{rarity:"00",owned:false, uptied:'0'},
                "Shi Assoc. South Section 5 Ishmael":{rarity:"00",owned:false, uptied:'0'},
                "LCCB Assistant Manager Ishmael":{rarity:"00",owned:false, uptied:'0'},
                "LCB Sinner Ishmael":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs: {
                "Snagharpoon":{rarity:"Z",owned:false, uptied:'0'},
                "Roseate Desire":{rarity:"T",owned:false, uptied:'0'},
                "Capote":{rarity:"T",owned:false, uptied:'0'},
                "Ardor Blossom Star":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        RodionIDs: {
            IDs:{
                "Kurokumo Clan Wakashu Rodion":{rarity:"000",owned:false, uptied:'0'},
                "Rosespanner Workshop Rep Rodion":{rarity:"000",owned:false, uptied:'0'},
                "Dieci Assoc. South Section 4 Rodion":{rarity:"000",owned:false, uptied:'0'},
                "LCCB Assistant Manager Rodion":{rarity:"00",owned:false, uptied:'0'},
                "Zwei Assoc. South Section 5 Rodion":{rarity:"00",owned:false, uptied:'0'},
                "N Corp. Mittelhammer Rodion":{rarity:"00",owned:false, uptied:'0'},
                "LCB Sinner Rodion":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs: {
                "What is Cast":{rarity:"Z",owned:false, uptied:'0'},
                "Rime Shank":{rarity:"T",owned:false, uptied:'0'},
                "4th Match Flame":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        SinclairIDs: {
            IDs:{
                "Blade Lineage Salsu Sinclair":{rarity:"000",owned:false, uptied:'0'},
                "The One Who Shall Grip Sinclair":{rarity:"000",owned:false, uptied:'0'},
                "Zwei Assoc. South Section 6 Sinclair":{rarity:"00",owned:false, uptied:'0'},
                "Los Mariachis Jefe Sinclair":{rarity:"00",owned:false, uptied:'0'},
                "Lobotomy E.G.O::Red Sheet Sinclair":{rarity:"00",owned:false, uptied:'0'},
                "Molar Boatworks Fixer Sinclair":{rarity:"00",owned:false, uptied:'0'},
                "LCB Sinner Sinclair":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs: {
                "Branch of Knowledge":{rarity:"Z",owned:false, uptied:'0'},
                "Impending Day":{rarity:"T",owned:false, uptied:'0'},
                "Lifetime Stew":{rarity:"T",owned:false, uptied:'0'},
                "Lantern":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        OutisIDs: {
            IDs:{
                "Seven Assoc. South Section 6 Director Outis":{rarity:"000",owned:false, uptied:'0'},
                "Molar Office Fixer Outis":{rarity:"000",owned:false, uptied:'0'},
                "G Corp. Head Manager Outis":{rarity:"00",owned:false, uptied:'0'},
                "Blade Lineage Cutthroat Outis":{rarity:"00",owned:false, uptied:'0'},
                "LCB Sinner Outis":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs: {
                "To pathos Mathos":{rarity:"Z",owned:false, uptied:'0'},
                "Sunshower":{rarity:"T",owned:false, uptied:'0'},
                "Ya Sunyata Tad Rupam":{rarity:"T",owned:false, uptied:'0'},
                "Ebony Stem":{rarity:"H",owned:false, uptied:'0'},
            },
        },
        GregorIDs: {
            IDs: {
                "G Corp. Manager Corporal Gregor":{rarity:"000",owned:false, uptied:'0'},
                "Zwei Assoc. South Section 4 Gregor":{rarity:"000",owned:false, uptied:'0'},
                "Rosespanner Workshop Fixer Gregor":{rarity:"00",owned:false, uptied:'0'},
                "Liu Assoc. South Section 6 Gregor":{rarity:"00",owned:false, uptied:'0'},
                "R.B. Sous-chef Gregor":{rarity:"00",owned:false, uptied:'0'},
                "LCB Sinner Gregor":{rarity:"0",owned:false, uptied:'0'},
            },
            EGOs: {
                "Suddenly,One Day":{rarity:"Z",owned:false, uptied:'0'},
                "Legerdemain":{rarity:"Z",owned:false, uptied:'0'},
                "AEDD":{rarity:"T",owned:false, uptied:'0'},
                "Lantern":{rarity:"H",owned:false, uptied:'0'},
            },
        },
    }
  },
  computed: {
    currentID(){
        return this.currentselected.id;
    },
    currentIDName(){
        return this.currentselected.name;
    },
    currentIDList(){
        var path;
        switch(this.currentselected.id) {
            case "YiSangIDs":
                path = this.YiSangIDs;
                break;
            case "FaustIDs":
                path = this.FaustIDs;
                break;
            case "DonIDs":
                path = this.DonIDs;
                break;
            case "RyoshuIDs":
                path = this.RyoshuIDs;
                break;
            case "MeurIDs":
                path = this.MeurIDs;
                break;
            case "HongLuIDs":
                path = this.HongLuIDs;
                break;
            case "HeathIDs":
                path = this.HeathIDs;
                break;
            case "IshIDs":
                path = this.IshIDs;
                break;
            case "RodionIDs":
                path = this.RodionIDs;
                break;
            case "SinclairIDs":
                path = this.SinclairIDs;
                break;
            case "OutisIDs":
                path = this.OutisIDs;
                break;
            case "GregorIDs":
                path = this.GregorIDs;
                break;
        }
        return path;
    }
  },
  methods: {
    //for debugging
    testing(){
        console.log(this.$data);
    },
    
    //update the current id
    getIDselected(){
        var e = document.getElementById("IDs-select");
        this.currentselected.id = e.value;
        this.currentselected.name = e.options[e.selectedIndex].text;
        localStorage.setItem("CurrentID", e.value);
    },
    
    //for getting the option value
    getitemselected(item){
        var e = document.getElementById(item);
        return e.value;
    },
  },
  components: {
  },
  watch:{
  }
}
</script>

<style>

select {
    appearance: none;
    /* safari */
    -webkit-appearance: none;
    /* other styles for aesthetics */
    width: 30%;
    font-size: 1rem;
    padding: 0.675em 6em 0.675em 1em;
    background-color: #fff;
    border: 1px solid #caced1;
    border-radius: 0.25rem;
    color: #000;
    cursor: pointer;
  }

</style>
  

  