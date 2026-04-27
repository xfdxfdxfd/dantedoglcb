<template>
    <div class="page-shell">
        <section class="mx-auto max-w-5xl px-4 py-8 md:px-6 lg:px-8">
            <div class="content-card overflow-hidden px-6 py-8 md:px-8">
                <p class="field-label text-gold">Release Notes</p>
                <h1 class="section-title mt-3">{{ $t(`Changelog`) }}</h1>
                <div class="mt-8 space-y-4">
                    <article v-for="entry in timelineEntries" :key="entry.date" class="rounded-[1.75rem] border p-5" :class="entry.tone === 'dark' ? 'border-white/10 bg-black/20' : 'border-gold/20 bg-amber-300/10'">
                        <p class="text-sm font-semibold uppercase tracking-[0.22em]" :class="entry.tone === 'dark' ? 'text-gold' : 'text-amber-200'">{{ entry.date }}</p>
                        <p class="mt-3 text-sm leading-7 text-stone-200">{{ $t(`Changelog${entry.date}`) }}</p>
                    </article>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: 'Changelog',
    data() {
        return {
            UpdateDate2024: ["22-05-2024", "03-05-2024", "23-04-2024", "31-03-2024", "19-03-2024", "07-03-2024", "17-02-2024", "07-02-2024", "24-01-2024", "10-01-2024"],
            UpdateDate2023: ["22-12-2023", "18-12-2023", "12-12-2023", "06-12-2023", "30-11-2023", "26-11-2023", "22-11-2023", "21-11-2023", "19-11-2023"],
        }
    },
    computed: {
        timelineEntries() {
            return [
                ...this.UpdateDate2024.map((date) => ({ date, tone: 'dark' })),
                ...this.UpdateDate2023.map((date) => ({ date, tone: 'warm' })),
            ];
        },
    }
}
</script>
