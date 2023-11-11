<template>
    <div style="min-height: 100vh;" class="content">
        <div style="position: relative;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{$t(`StatusSetting`)}}</h1>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <div>
                    <select style="width: 80%;background-color: rgb(255, 220, 161);">
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
                <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`YiSang`)}}</h2>
                <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in YiSangIDs" :key="index">
                    {{$t(index)}}
                    &nbsp;
                    <div >
                        <select id="uptieIDs-select">
                            <option value="Don't have">{{$t(`Don't have`)}}</option>
                            <option value="Uptie1">{{$t(`Uptie`)}}1</option>
                            <option value="Uptie2">{{$t(`Uptie`)}}2</option>
                            <option value="Uptie3">{{$t(`Uptie`)}}3</option>
                            <option value="Uptie4">{{$t(`Uptie`)}}4</option>
                        </select>
                    </div>
                    &nbsp;
                </li>
                <h2 class="box1h2text">{{$t(`Faust`)}}</h2>
                <div  style="text-align: left;padding-left:150px" v-for="(id, index) in FaustIDs" :key="id">
                    {{$t(index)}}
                    &nbsp;
                    <div >
                        <select id="standard-select">
                            <option value="Don't have">{{$t(`Don't have`)}}</option>
                            <option value="Uptie1">{{$t(`Uptie`)}}1</option>
                            <option value="Uptie2">{{$t(`Uptie`)}}2</option>
                            <option value="Uptie3">{{$t(`Uptie`)}}3</option>
                            <option value="Uptie4">{{$t(`Uptie`)}}4</option>
                        </select>
                    </div>
                    &nbsp;
                    <span class="focus"></span>
                </div>

                <button @click="testing()">Submit</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'StatusSetting',
  data(){
    return {
        YiSangIDs: {
                "Effloresced E.G.O::Spicebush YiSang": {rarity:"000",owned:false, uptied:1},
                "Blade Lineage Salsu YiSang": {rarity:"000",owned:false, uptied:1},
                "W Corp. L3 Cleanup Agent YiSang": {rarity:"000",owned:false, uptied:1},
                "Seven Assoc. South Section 6 YiSang":{rarity:"00",owned:false,uptied:1},
                "Molar Office Fixer YiSang":{rarity:"00",owned:false,uptied:1},
                "LCB Sinner YiSang":{rarity:"0",owned:false, uptied:1},
            },
        FaustIDs: {
            "Seven Assoc. South Section 4 Faust": {rarity:"000",owned:false, uptied:1},
            "The One Who Grips Faust": {rarity:"000",owned:false, uptied:1},
            "Lobotomy E.G.O::Regret Faust": {rarity:"000",owned:false, uptied:1},
            "Lobotomy Corp Remnant Faust": {rarity:"00",owned:false, uptied:1},
            "W Corp. L2 Cleanup Agent Faust": {rarity:"00",owned:false, uptied:1},
            "Zwei Assoc. South Section 4 Faust": {rarity:"00",owned:false, uptied:1},
            "LCB Sinner Faust":{rarity:"0",owned:false, uptied:1},
        },
        DonIDs: {
            "Cinq Assoc. South Section 5 Director Don Quixote": {rarity:"000",owned:false, uptied:1},
            "W Corp. L3 Cleanup Agent Don Quixote": {rarity:"000",owned:false, uptied:1},
            "Shi Assoc. South Section 5 Director Don Quixote":{rarity:"00",owned:false,uptied:1},
            "N Corp. Mittelhammer Don Quixote":{rarity:"00",owned:false,uptied:1},
            "LCB Sinner Don Quixote":{rarity:"0",owned:false, uptied:1},
        },
        RyoshuIDs: {
            "W Corp. L3 Cleanup Agent Ryoshu": {rarity:"000",owned:false, uptied:1},
            "R.B. Chef de Cuisine Ryoshu": {rarity:"000",owned:false, uptied:1},
            "Kurokumo Clan Wakashu Ryoshu": {rarity:"000",owned:false, uptied:1},
            "Seven Assoc. South Section 6 Ryoshu": {rarity:"00",owned:false, uptied:1},
            "LCB Sinner Ryoshu":{rarity:"0",owned:false, uptied:1},
        },
        MeurIDs: {
            "R Corp. 4th Pack Rhino Meursault": {rarity:"000",owned:false, uptied:1},
            "N Corp. GroBHammer Meursault": {rarity:"000",owned:false, uptied:1},
            "W Corp. L2 Cleanup Agent Meursault": {rarity:"000",owned:false, uptied:1},
            "Liu Assoc. South Section 6 Meursault": {rarity:"00",owned:false, uptied:1},
            "Rosespanner Workshop Fixer Meursault": {rarity:"00",owned:false, uptied:1},
            "LCB Sinner Meursault":{rarity:"0",owned:false, uptied:1},
        },
        HongLuIDs: {
            "Ting Tang Gang Gangleader Hong Lu": {rarity:"000",owned:false, uptied:1},
            "K Corp. Class 3 Excision Staff Hong Lu": {rarity:"000",owned:false, uptied:1},
            "Kurokumo Clan Wakashu Hong Lu": {rarity:"00",owned:false, uptied:1},
            "W Corp. L2 Cleanup Agent Hong Lu": {rarity:"00",owned:false, uptied:1},
            "Liu Assoc. South Section 5 Hong Lu": {rarity:"00",owned:false, uptied:1},
            "Hook Office Fixer Hong Lu": {rarity:"00",owned:false, uptied:1},
            "LCB Sinner Hong Lu":{rarity:"0",owned:false, uptied:1},
        },
        HeathIDs: {
            "R Corp. 4th Pack Rabbit Heathcliff": {rarity:"000",owned:false, uptied:1},
            "Lobotomy E.G.O::Sunshower Heathcliff": {rarity:"000",owned:false, uptied:1},
            "Shi Assoc. South Section 5 Heathcliff":{rarity:"00",owned:false,uptied:1},
            "Seven Assoc. South Section 4 Heathcliff":{rarity:"00",owned:false,uptied:1},
            "N Corp. Kleinhammer Heathcliff":{rarity:"00",owned:false,uptied:1},
            "LCB Sinner Heathcliff":{rarity:"0",owned:false, uptied:1},
        },
        IshIDs: {
            "Molar Boatworks Fixer Ishmael":{rarity:"000",owned:false, uptied:1},
            "R Corp. 4th Pack Reindeer Ishmael":{rarity:"000",owned:false, uptied:1},
            "Liu Assoc. South Section 4 Ishmael":{rarity:"000",owned:false, uptied:1},
            "Lobotomy E.G.O::Sloshing Ishmael":{rarity:"00",owned:false, uptied:1},
            "Shi Assoc. South Section 5 Ishmael":{rarity:"00",owned:false, uptied:1},
            "LCCB Assistant Manager Ishmael":{rarity:"00",owned:false, uptied:1},
            "LCB Sinner Ishmael":{rarity:"0",owned:false, uptied:1},
        },
        RodionIDs: {
            "Kurokumo Clan Wakashu Rodion":{rarity:"000",owned:false, uptied:1},
            "Rosespanner Workshop Rep Rodion":{rarity:"000",owned:false, uptied:1},
            "Dieci Assoc. South Section 4 Rodion":{rarity:"000",owned:false, uptied:1},
            "LCCB Assistant Manager Rodion":{rarity:"00",owned:false, uptied:1},
            "Zwei Assoc. South Section 5 Rodion":{rarity:"00",owned:false, uptied:1},
            "N Corp. Mittelhammer Rodion":{rarity:"00",owned:false, uptied:1},
            "LCB Sinner Rodion":{rarity:"0",owned:false, uptied:1},
        },
        SinclairIDs: {
            "Blade Lineage Salsu Sinclair":{rarity:"000",owned:false, uptied:1},
            "The One Who Shall Grip Sinclair":{rarity:"000",owned:false, uptied:1},
            "Zwei Assoc. South Section 6 Sinclair":{rarity:"00",owned:false, uptied:1},
            "Los Mariachis Jefe Sinclair":{rarity:"00",owned:false, uptied:1},
            "Lobotomy E.G.O::Red Sheet Sinclair":{rarity:"00",owned:false, uptied:1},
            "Molar Boatworks Fixer Sinclair":{rarity:"00",owned:false, uptied:1},
            "LCB Sinner Sinclair":{rarity:"0",owned:false, uptied:1},
        },
        OutisIDs: {
            "Seven Assoc. South Section 6 Director Outis":{rarity:"000",owned:false, uptied:1},
            "Molar Office Fixer Outis":{rarity:"000",owned:false, uptied:1},
            "G Corp. Head Manager Outis":{rarity:"00",owned:false, uptied:1},
            "Blade Lineage Cutthroat Outis":{rarity:"00",owned:false, uptied:1},
            "LCB Sinner Outis":{rarity:"0",owned:false, uptied:1},
        },
        GregorIDs: {
            "G Corp. Manager Corporal Gregor":{rarity:"000",owned:false, uptied:1},
            "Zwei Assoc. South Section 4 Gregor":{rarity:"000",owned:false, uptied:1},
            "Rosespanner Workshop Fixer Gregor":{rarity:"00",owned:false, uptied:1},
            "Liu Assoc. South Section 6 Gregor":{rarity:"00",owned:false, uptied:1},
            "R.B. Sous-chef Gregor":{rarity:"00",owned:false, uptied:1},
            "LCB Sinner Gregor":{rarity:"0",owned:false, uptied:1},
        },
        EGOs :{
            YiSangEGOs: {
            },
            FaustEGOs: {
            },
            DonEGOs: {
            },
            RyoshuEGOs: {
            },
            MeurEGOs: {
            },
            HongLuEGOs: {
            },
            HeathEGOs: {
            },
            IshEGOs: {
            },
            RodionEGOs: {
            },
            SinclairEGOs: {
            },
            OutisEGOs: {
            },
            GregorEGOs: {
            },
        }

    }
  },
  computed: {
  },
  methods: {
    testing(){
        console.log(this.IDs)
    }
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
  

  