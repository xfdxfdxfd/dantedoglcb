<template>
    <div style="min-height: 100vh;" class="content">
        <div style="position: relative;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{$t(`StatusSetting`)}}</h1>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <button @click="testing()">Testing</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'StatusSetting',
  data(){
    return {
        IDs: {
            YiSangIDs: {
                Rarity000 :{
                    "Effloresced E.G.O::Spicebush YiSang": {owned:false, uptied:1},
                    "Blade Lineage Salsu YiSang": {owned:false, uptied:1},
                    "W Corp. L3 Cleanup Agent YiSang": {owned:false, uptied:1},

                },
                Rarity00 :{
                    "Seven Assoc. South Section 6 YiSang":{owned:false,uptied:1},
                    "Molar Office Fixer YiSang":{owned:false,uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner YiSang":{owned:false, uptied:1},
                }
            },
            FaustIDs: {
                Rarity000 :{
                    "Seven Assoc. South Section 4 Faust": {owned:false, uptied:1},
                    "The One Who Grips Faust": {owned:false, uptied:1},
                    "Lobotomy E.G.O::Regret Faust": {owned:false, uptied:1},

                },
                Rarity00 :{
                    "Lobotomy Corp Remnant Faust": {owned:false, uptied:1},
                    "W Corp. L2 Cleanup Agent Faust": {owned:false, uptied:1},
                    "Zwei Assoc. South Section 4 Faust": {owned:false, uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Faust":{owned:false, uptied:1},
                }
            },
            DonIDs: {
                Rarity000 :{
                    "Cinq Assoc. South Section 5 Director Don Quixote": {owned:false, uptied:1},
                    "W Corp. L3 Cleanup Agent Don Quixote": {owned:false, uptied:1},

                },
                Rarity00 :{
                    "Shi Assoc. South Section 5 Director Don Quixote":{owned:false,uptied:1},
                    "N Corp. Mittelhammer Don Quixote":{owned:false,uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Don Quixote":{owned:false, uptied:1},
                }
            },
            RyoshuIDs: {
                Rarity000 :{
                    "W Corp. L3 Cleanup Agent Ryoshu": {owned:false, uptied:1},
                    "R.B. Chef de Cuisine Ryoshu": {owned:false, uptied:1},
                    "Kurokumo Clan Wakashu Ryoshu": {owned:false, uptied:1},

                },
                Rarity00 :{
                    "Seven Assoc. South Section 6 Ryoshu": {owned:false, uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Ryoshu":{owned:false, uptied:1},
                }
            },
            MeurIDs: {
                Rarity000 :{
                    "R Corp. 4th Pack Rhino Meursault": {owned:false, uptied:1},
                    "N Corp. GroBHammer Meursault": {owned:false, uptied:1},
                    "W Corp. L2 Cleanup Agent Meursault": {owned:false, uptied:1},

                },
                Rarity00 :{
                    "Liu Assoc. South Section 6 Meursault": {owned:false, uptied:1},
                    "Rosespanner Workshop Fixer Meursault": {owned:false, uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Meursault":{owned:false, uptied:1},
                }
            },
            HongLuIDs: {
                Rarity000 :{
                    "Ting Tang Gang Gangleader Hong Lu": {owned:false, uptied:1},
                    "K Corp. Class 3 Excision Staff Hong Lu": {owned:false, uptied:1},

                },
                Rarity00 :{
                    "Kurokumo Clan Wakashu Hong Lu": {owned:false, uptied:1},
                    "W Corp. L2 Cleanup Agent Hong Lu": {owned:false, uptied:1},
                    "Liu Assoc. South Section 5 Hong Lu": {owned:false, uptied:1},
                    "Hook Office Fixer Hong Lu": {owned:false, uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Hong Lu":{owned:false, uptied:1},
                }
            },
            HeathIDs: {
                Rarity000 :{
                    "R Corp. 4th Pack Rabbit Heathcliff": {owned:false, uptied:1},
                    "Lobotomy E.G.O::Sunshower Heathcliff": {owned:false, uptied:1},

                },
                Rarity00 :{
                    "Shi Assoc. South Section 5 Heathcliff":{owned:false,uptied:1},
                    "Seven Assoc. South Section 4 Heathcliff":{owned:false,uptied:1},
                    "N Corp. Kleinhammer Heathcliff":{owned:false,uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Heathcliff":{owned:false, uptied:1},
                }
            },
            IshIDs: {
                Rarity000 :{
                    "Molar Boatworks Fixer Ishmael":{owned:false, uptied:1},
                    "R Corp. 4th Pack Reindeer Ishmael":{owned:false, uptied:1},
                    "Liu Assoc. South Section 4 Ishmael":{owned:false, uptied:1},
                },
                Rarity00 :{
                    "Lobotomy E.G.O::Sloshing Ishmael":{owned:false, uptied:1},
                    "Shi Assoc. South Section 5 Ishmael":{owned:false, uptied:1},
                    "LCCB Assistant Manager Ishmael":{owned:false, uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Ishmael":{owned:false, uptied:1},
                }
            },
            RodionIDs: {
                Rarity000 :{
                    "Kurokumo Clan Wakashu Rodion":{owned:false, uptied:1},
                    "Rosespanner Workshop Rep Rodion":{owned:false, uptied:1},
                    "Dieci Assoc. South Section 4 Rodion":{owned:false, uptied:1},

                },
                Rarity00 :{
                    "LCCB Assistant Manager Rodion":{owned:false, uptied:1},
                    "Zwei Assoc. South Section 5 Rodion":{owned:false, uptied:1},
                    "N Corp. Mittelhammer Rodion":{owned:false, uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Rodion":{owned:false, uptied:1},
                }
            },
            SinclairIDs: {
                Rarity000 :{
                    "Blade Lineage Salsu Sinclair":{owned:false, uptied:1},
                    "The One Who Shall Grip Sinclair":{owned:false, uptied:1},

                },
                Rarity00 :{
                    "Zwei Assoc. South Section 6 Sinclair":{owned:false, uptied:1},
                    "Los Mariachis Jefe Sinclair":{owned:false, uptied:1},
                    "Lobotomy E.G.O::Red Sheet Sinclair":{owned:false, uptied:1},
                    "Molar Boatworks Fixer Sinclair":{owned:false, uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Sinclair":{owned:false, uptied:1},
                }
            },
            OutisIDs: {
                Rarity000 :{
                    "Seven Assoc. South Section 6 Director Outis":{owned:false, uptied:1},
                    "Molar Office Fixer Outis":{owned:false, uptied:1},

                },
                Rarity00 :{
                    "G Corp. Head Manager Outis":{owned:false, uptied:1},
                    "Blade Lineage Cutthroat Outis":{owned:false, uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Outis":{owned:false, uptied:1},
                }
            },
            GregorIDs: {
                Rarity000 :{
                    "G Corp. Manager Corporal Gregor":{owned:false, uptied:1},
                    "Zwei Assoc. South Section 4 Gregor":{owned:false, uptied:1},

                },
                Rarity00 :{
                    "Rosespanner Workshop Fixer Gregor":{owned:false, uptied:1},
                    "Liu Assoc. South Section 6 Gregor":{owned:false, uptied:1},
                    "R.B. Sous-chef Gregor":{owned:false, uptied:1},
                },
                Rarity0 :{
                    "LCB Sinner Gregor":{owned:false, uptied:1},
                }
            },
        },
        EGOs :{
            YiSangEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            FaustEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            DonEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            RyoshuEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            MeurEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            HongLuEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            HeathEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            IshEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            RodionEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            SinclairEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            OutisEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

            },
            GregorEGOs: {
                Z:{

                },
                T:{

                },
                H:{

                }

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

<style></style>