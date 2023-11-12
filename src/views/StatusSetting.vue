<template>
    <div style="min-height: 100vh;" class="content">
        <div style="position: relative;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{$t(`StatusSetting`)}}</h1>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <div>
                    <select id="IDs-select" style="width: 80%;background-color: rgb(255, 220, 161);" @change="getitemselected('IDs-select')">
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
                <template v-if="currentselected.id == 'YiSangIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`YiSang`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in YiSangIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in YiSangEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'FaustIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Faust`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in FaustIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in FaustEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'DonIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Don Quixote`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in DonIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in DonEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'RyoshuIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Ryoshu`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in RyoshuIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in RyoshuEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'MeurIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Meursault`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in MeurIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in MeurEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'HongLuIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Hong Lu`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in HongLuIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in HongLuEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'HeathIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Heathcliff`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in HeathIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in HeathEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'IshIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Ishmael`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in IshIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in IshEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'RodionIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Rodion`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in RodionIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in RodionEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'SinclairIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Sinclair`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in SinclairIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in SinclairEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'OutisIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Outis`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in OutisIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in OutisEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>
                <template v-if="currentselected.id == 'GregorIDs'">
                    <h2 class="box1h2text" style="font-size: 2.2rem;">{{$t(`Gregor`)}}</h2>
                    <h3 class="box1h3text" style="text-align: left;font-size: 1.5rem">{{$t(`Identities`)}}</h3>
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in GregorIDs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+index' @change="getitemselected(currentselected.id+index)">
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
                    <li  style="text-align: left;padding-left:150px;font-size: 1.15rem" v-for="(id, index) in GregorEGOs" :key="index">
                        {{$t(index)}}
                        &nbsp;
                        <div >
                            <select :id='currentselected.id+"EGO"+index' @change="getitemselected(currentselected.id+'EGO'+index)">
                                <option value="0">{{$t(`Don't have`)}}</option>
                                <option value="1">{{$t(`Uptie`)}}1</option>
                                <option value="2">{{$t(`Uptie`)}}2</option>
                                <option value="3">{{$t(`Uptie`)}}3</option>
                                <option value="4">{{$t(`Uptie`)}}4</option>
                            </select>
                        </div>
                        &nbsp;
                    </li>
                </template>




                <button @click="testing()">Submit</button>
            </div>
        </div>
    </div>
</template>

<script>
import { stringifyQuery } from 'vue-router';
export default {
  name: 'StatusSetting',
  props: ['StatusData'],
  data(){
    return {
        currentselected:{id:"YiSangIDs",name:"YiSang"},
        YiSangIDs: {
                "Effloresced E.G.O::Spicebush YiSang": {rarity:"000",owned:false, uptied:'0'},
                "Blade Lineage Salsu YiSang": {rarity:"000",owned:false, uptied:'0'},
                "W Corp. L3 Cleanup Agent YiSang": {rarity:"000",owned:false, uptied:'0'},
                "Seven Assoc. South Section 6 YiSang":{rarity:"00",owned:false,uptied:'0'},
                "Molar Office Fixer YiSang":{rarity:"00",owned:false,uptied:'0'},
                "LCB Sinner YiSang":{rarity:"0",owned:false, uptied:'0'},
            },
        FaustIDs: {
            "Seven Assoc. South Section 4 Faust": {rarity:"000",owned:false, uptied:'0'},
            "The One Who Grips Faust": {rarity:"000",owned:false, uptied:'0'},
            "Lobotomy E.G.O::Regret Faust": {rarity:"000",owned:false, uptied:'0'},
            "Lobotomy Corp Remnant Faust": {rarity:"00",owned:false, uptied:'0'},
            "W Corp. L2 Cleanup Agent Faust": {rarity:"00",owned:false, uptied:'0'},
            "Zwei Assoc. South Section 4 Faust": {rarity:"00",owned:false, uptied:'0'},
            "LCB Sinner Faust":{rarity:"0",owned:false, uptied:'0'},
        },
        DonIDs: {
            "Cinq Assoc. South Section 5 Director Don Quixote": {rarity:"000",owned:false, uptied:'0'},
            "W Corp. L3 Cleanup Agent Don Quixote": {rarity:"000",owned:false, uptied:'0'},
            "Shi Assoc. South Section 5 Director Don Quixote":{rarity:"00",owned:false,uptied:'0'},
            "N Corp. Mittelhammer Don Quixote":{rarity:"00",owned:false,uptied:'0'},
            "LCB Sinner Don Quixote":{rarity:"0",owned:false, uptied:'0'},
        },
        RyoshuIDs: {
            "W Corp. L3 Cleanup Agent Ryoshu": {rarity:"000",owned:false, uptied:'0'},
            "R.B. Chef de Cuisine Ryoshu": {rarity:"000",owned:false, uptied:'0'},
            "Kurokumo Clan Wakashu Ryoshu": {rarity:"000",owned:false, uptied:'0'},
            "Seven Assoc. South Section 6 Ryoshu": {rarity:"00",owned:false, uptied:'0'},
            "LCB Sinner Ryoshu":{rarity:"0",owned:false, uptied:'0'},
        },
        MeurIDs: {
            "R Corp. 4th Pack Rhino Meursault": {rarity:"000",owned:false, uptied:'0'},
            "N Corp. GroBHammer Meursault": {rarity:"000",owned:false, uptied:'0'},
            "W Corp. L2 Cleanup Agent Meursault": {rarity:"000",owned:false, uptied:'0'},
            "Liu Assoc. South Section 6 Meursault": {rarity:"00",owned:false, uptied:'0'},
            "Rosespanner Workshop Fixer Meursault": {rarity:"00",owned:false, uptied:'0'},
            "LCB Sinner Meursault":{rarity:"0",owned:false, uptied:'0'},
        },
        HongLuIDs: {
            "Ting Tang Gang Gangleader Hong Lu": {rarity:"000",owned:false, uptied:'0'},
            "K Corp. Class 3 Excision Staff Hong Lu": {rarity:"000",owned:false, uptied:'0'},
            "Kurokumo Clan Wakashu Hong Lu": {rarity:"00",owned:false, uptied:'0'},
            "W Corp. L2 Cleanup Agent Hong Lu": {rarity:"00",owned:false, uptied:'0'},
            "Liu Assoc. South Section 5 Hong Lu": {rarity:"00",owned:false, uptied:'0'},
            "Hook Office Fixer Hong Lu": {rarity:"00",owned:false, uptied:'0'},
            "LCB Sinner Hong Lu":{rarity:"0",owned:false, uptied:'0'},
        },
        HeathIDs: {
            "R Corp. 4th Pack Rabbit Heathcliff": {rarity:"000",owned:false, uptied:'0'},
            "Lobotomy E.G.O::Sunshower Heathcliff": {rarity:"000",owned:false, uptied:'0'},
            "Shi Assoc. South Section 5 Heathcliff":{rarity:"00",owned:false,uptied:'0'},
            "Seven Assoc. South Section 4 Heathcliff":{rarity:"00",owned:false,uptied:'0'},
            "N Corp. Kleinhammer Heathcliff":{rarity:"00",owned:false,uptied:'0'},
            "LCB Sinner Heathcliff":{rarity:"0",owned:false, uptied:'0'},
        },
        IshIDs: {
            "Molar Boatworks Fixer Ishmael":{rarity:"000",owned:false, uptied:'0'},
            "R Corp. 4th Pack Reindeer Ishmael":{rarity:"000",owned:false, uptied:'0'},
            "Liu Assoc. South Section 4 Ishmael":{rarity:"000",owned:false, uptied:'0'},
            "Lobotomy E.G.O::Sloshing Ishmael":{rarity:"00",owned:false, uptied:'0'},
            "Shi Assoc. South Section 5 Ishmael":{rarity:"00",owned:false, uptied:'0'},
            "LCCB Assistant Manager Ishmael":{rarity:"00",owned:false, uptied:'0'},
            "LCB Sinner Ishmael":{rarity:"0",owned:false, uptied:'0'},
        },
        RodionIDs: {
            "Kurokumo Clan Wakashu Rodion":{rarity:"000",owned:false, uptied:'0'},
            "Rosespanner Workshop Rep Rodion":{rarity:"000",owned:false, uptied:'0'},
            "Dieci Assoc. South Section 4 Rodion":{rarity:"000",owned:false, uptied:'0'},
            "LCCB Assistant Manager Rodion":{rarity:"00",owned:false, uptied:'0'},
            "Zwei Assoc. South Section 5 Rodion":{rarity:"00",owned:false, uptied:'0'},
            "N Corp. Mittelhammer Rodion":{rarity:"00",owned:false, uptied:'0'},
            "LCB Sinner Rodion":{rarity:"0",owned:false, uptied:'0'},
        },
        SinclairIDs: {
            "Blade Lineage Salsu Sinclair":{rarity:"000",owned:false, uptied:'0'},
            "The One Who Shall Grip Sinclair":{rarity:"000",owned:false, uptied:'0'},
            "Zwei Assoc. South Section 6 Sinclair":{rarity:"00",owned:false, uptied:'0'},
            "Los Mariachis Jefe Sinclair":{rarity:"00",owned:false, uptied:'0'},
            "Lobotomy E.G.O::Red Sheet Sinclair":{rarity:"00",owned:false, uptied:'0'},
            "Molar Boatworks Fixer Sinclair":{rarity:"00",owned:false, uptied:'0'},
            "LCB Sinner Sinclair":{rarity:"0",owned:false, uptied:'0'},
        },
        OutisIDs: {
            "Seven Assoc. South Section 6 Director Outis":{rarity:"000",owned:false, uptied:'0'},
            "Molar Office Fixer Outis":{rarity:"000",owned:false, uptied:'0'},
            "G Corp. Head Manager Outis":{rarity:"00",owned:false, uptied:'0'},
            "Blade Lineage Cutthroat Outis":{rarity:"00",owned:false, uptied:'0'},
            "LCB Sinner Outis":{rarity:"0",owned:false, uptied:'0'},
        },
        GregorIDs: {
            "G Corp. Manager Corporal Gregor":{rarity:"000",owned:false, uptied:'0'},
            "Zwei Assoc. South Section 4 Gregor":{rarity:"000",owned:false, uptied:'0'},
            "Rosespanner Workshop Fixer Gregor":{rarity:"00",owned:false, uptied:'0'},
            "Liu Assoc. South Section 6 Gregor":{rarity:"00",owned:false, uptied:'0'},
            "R.B. Sous-chef Gregor":{rarity:"00",owned:false, uptied:'0'},
            "LCB Sinner Gregor":{rarity:"0",owned:false, uptied:'0'},
        },
        YiSangEGOs: {
            "Crow's Eye View":{rarity:"Z",owned:false, uptied:'0'},
            "4th Match Flame":{rarity:"T",owned:false, uptied:'0'},
            "Wishing Cairn":{rarity:"T",owned:false, uptied:'0'},
            "Dimension Shredder":{rarity:"H",owned:false, uptied:'0'},
            "Sunshower":{rarity:"H",owned:false, uptied:'0'}
        },
        FaustEGOs: {
            "Representation Emitter":{rarity:"Z",owned:false, uptied:'0'},
            "Hex Nail":{rarity:"T",owned:false, uptied:'0'},
            "Telepole":{rarity:"H",owned:false, uptied:'0'},
            "Fluid Sac":{rarity:"H",owned:false, uptied:'0'},
        },
        DonEGOs: {
            "La Sangre de Sancho":{rarity:"Z",owned:false, uptied:'0'},
            "Lifetime Stew":{rarity:"T",owned:false, uptied:'0'},
            "Fluid Sac":{rarity:"H",owned:false, uptied:'0'},
            "Telepole":{rarity:"H",owned:false, uptied:'0'},
        },
        RyoshuEGOs: {
            "Forest for the Flames":{rarity:"Z",owned:false, uptied:'0'},
            "Soda":{rarity:"Z",owned:false, uptied:'0'},
            "Red Eyes":{rarity:"T",owned:false, uptied:'0'},
            "4th Match Flame":{rarity:"H",owned:false, uptied:'0'},
            "Red Eyes (Open)":{rarity:"H",owned:false, uptied:'0'},
        },
        MeurEGOs: {
            "Chains of Others":{rarity:"Z",owned:false, uptied:'0'},
            "Screwloose Wallop":{rarity:"T",owned:false, uptied:'0'},
            "Regret":{rarity:"T",owned:false, uptied:'0'},
            "Capote":{rarity:"H",owned:false, uptied:'0'},
            "Pursuance":{rarity:"H",owned:false, uptied:'0'},
        },
        HongLuEGOs: {
            "Land of Illusion":{rarity:"Z",owned:false, uptied:'0'},
            "Roseate Desire":{rarity:"T",owned:false, uptied:'0'},
            "Soda":{rarity:"T",owned:false, uptied:'0'},
            "Dimension Shredder":{rarity:"H",owned:false, uptied:'0'},
        },
        HeathEGOs: {
            "Bodysack":{rarity:"Z",owned:false, uptied:'0'},
            "AEDD":{rarity:"T",owned:false, uptied:'0'},
            "Ya Sunyata Tad Rupam":{rarity:"H",owned:false, uptied:'0'},
            "Telepole":{rarity:"H",owned:false, uptied:'0'},
        },
        IshEGOs: {
            "Snagharpoon":{rarity:"Z",owned:false, uptied:'0'},
            "Roseate Desire":{rarity:"T",owned:false, uptied:'0'},
            "Capote":{rarity:"T",owned:false, uptied:'0'},
            "Ardor Blossom Star":{rarity:"H",owned:false, uptied:'0'},
        },
        RodionEGOs: {
            "What is Cast":{rarity:"Z",owned:false, uptied:'0'},
            "Rime Shank":{rarity:"T",owned:false, uptied:'0'},
            "4th Match Flame":{rarity:"H",owned:false, uptied:'0'},
        },
        SinclairEGOs: {
            "Branch of Knowledge":{rarity:"Z",owned:false, uptied:'0'},
            "Impending Day":{rarity:"T",owned:false, uptied:'0'},
            "Lifetime Stew":{rarity:"T",owned:false, uptied:'0'},
            "Lantern":{rarity:"H",owned:false, uptied:'0'},
        },
        OutisEGOs: {
            "To pathos Mathos":{rarity:"Z",owned:false, uptied:'0'},
            "Sunshower":{rarity:"T",owned:false, uptied:'0'},
            "Ya Sunyata Tad Rupam":{rarity:"T",owned:false, uptied:'0'},
            "Ebony Stem":{rarity:"H",owned:false, uptied:'0'},
        },
        GregorEGOs: {
            "Suddenly,One Day":{rarity:"Z",owned:false, uptied:'0'},
            "Legerdemain":{rarity:"Z",owned:false, uptied:'0'},
            "AEDD":{rarity:"T",owned:false, uptied:'0'},
            "Lantern":{rarity:"H",owned:false, uptied:'0'},
        },

    }
  },
  computed: {
  },
  methods: {
    //for debugging
    testing(){
        //console.log(this);

    },

    //for getting the selected ID for deciding which to show
    getitemselected(item){
        var e = document.getElementById(item);

        //if it is changing the current id
        if(item == "IDs-select"){
            this.currentselected.id = e.value;
            this.currentselected.name = e.options[e.selectedIndex].text;
            localStorage.setItem("CurrentID", document.getElementById(item).value);
            //console.log("current selected:",this.currentselected);
        }
        else{
            var currentselectedid_item = item.replace(this.currentselected.id,'');
            switch(this.currentselected.id){
            case "YiSangIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.YiSangEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.YiSangIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "FaustIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.FaustEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.FaustIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "DonIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.DonEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.DonIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "RyoshuIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.RyoshuEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.RyoshuIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "MeurIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.MeurEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.MeurIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "HongLuIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.HongLuEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.HongLuIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "HeathIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.HeathEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.HeathIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "IshIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.IshEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.IshIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "RodionIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.RodionEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.RodionIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "SinclairIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.SinclairEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.SinclairIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "OutisIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.OutisEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.OutisIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;
            case "GregorIDs":
                if(currentselectedid_item.includes("EGO")){
                    //it is ego
                    currentselectedid_item = currentselectedid_item.replace("EGO",'');
                    Object.entries(this.GregorEGOs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});

                }else{
                    //it is id
                    Object.entries(this.GregorIDs).forEach(([key, value]) => {
                        if(key == currentselectedid_item){
                            value.uptied = document.getElementById(item).value
                            //console.log(`${key} ${value.uptied}`, document.getElementById(item).value); //console log the selected one
                            localStorage.setItem("temp_status",JSON.stringify(this.$data));
                        }});
                }
                break;                
            }
        }
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
  

  