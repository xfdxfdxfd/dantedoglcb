<template>
    <div class="content">
        <div>
            <div class="box box1">
                <h1 class="subtitle">{{ $t(`Changelog`) }}</h1>
                &nbsp;
                <h2 class="separator"></h2>
                &nbsp;
                <!-- timeline item -->
                <div v-for="date in UpdateDate2024" :key="date" class="timeline">
                    <div class="container black">
                        <div class="timelinecontent_black">
                            <h3 style="text-align:left;">{{ date }}</h3>
                            <p style="text-align:left;">{{ $t("Changelog" + date) }}
                            </p>

                        </div>
                    </div>
                </div>
                <div v-for="date in UpdateDate2023" :key="date" class="timeline">
                    <div class="container orange">
                        <div class="timelinecontent_white">
                            <h3 style="text-align:left;">{{ date }}</h3>
                            <p style="text-align:left;">{{ $t("Changelog" + date) }}
                            </p>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Changelog',
    data() {
        return {
            UpdateDate2024: ["03-05-2024", "23-04-2024", "31-03-2024", "19-03-2024", "07-03-2024", "17-02-2024", "07-02-2024", "24-01-2024", "10-01-2024"],
            UpdateDate2023: ["22-12-2023", "18-12-2023", "12-12-2023", "06-12-2023", "30-11-2023", "26-11-2023", "22-11-2023", "21-11-2023", "19-11-2023"],
        }
    },
    computed: {
    },
    methods: {
    },
    mounted() {
    }
}
</script>


<style>
@import '../components/format.css';
</style>
