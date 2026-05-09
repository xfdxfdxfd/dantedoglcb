const DEFAULT_UPTIE = '0';
const DEFAULT_LEVEL = 1;

function buildEntries(entries) {
    return Object.fromEntries(
        entries.map(([name, rarity]) => [
            name,
            {
                rarity,
                uptied: DEFAULT_UPTIE,
                level: DEFAULT_LEVEL,
            },
        ])
    );
}

export const rosterCatalog = {
    YiSangIDs: {
        IDs: [
            ['The Ring Pointillist Student Yi Sang', 'Rarity000'],
            ['Effloresced E.G.O::Spicebush YiSang', 'Rarity000'],
            ['Blade Lineage Salsu YiSang', 'Rarity000'],
            ['W Corp. L3 Cleanup Agent YiSang', 'Rarity000'],
            ['Seven Assoc. South Section 6 YiSang', 'Rarity00'],
            ['Molar Office Fixer YiSang', 'Rarity00'],
            ['The Pequod First Mate Yi Sang', 'Rarity00'],
            ['Dieci South Section 4 Yi Sang', 'Rarity00'],
            ['LCB Sinner YiSang', 'Rarity0'],
        ],
        EGOs: [
            ["Crow's Eye View", 'Z'],
            ['Bygone Days', 'ZnotOriginal'],
            ['4th Match Flame', 'T'],
            ['Wishing Cairn', 'T'],
            ['Dimension Shredder', 'H'],
            ['Sunshower', 'W'],
        ],
    },
    FaustIDs: {
        IDs: [
            ['Seven Assoc. South Section 4 Faust', 'Rarity000'],
            ['Blade Lineage Salsu Faust', 'Rarity000'],
            ['The One Who Grips Faust', 'Rarity000'],
            ['Lobotomy E.G.O::Regret Faust', 'Rarity000'],
            ['Lobotomy Corp Remnant Faust', 'Rarity00'],
            ['W Corp. L2 Cleanup Agent Faust', 'Rarity00'],
            ['Wuthering Heights Butler Faust', 'Rarity00'],
            ['Zwei Assoc. South Section 4 Faust', 'Rarity00'],
            ['LCB Sinner Faust', 'Rarity0'],
        ],
        EGOs: [
            ['Representation Emitter', 'Z'],
            ['Hex Nail', 'T'],
            ['9:2', 'T'],
            ['Telepole', 'H'],
            ['Fluid Sac', 'H'],
        ],
    },
    DonIDs: {
        IDs: [
            ['Cinq Assoc. South Section 5 Director Don Quixote', 'Rarity000'],
            ['W Corp. L3 Cleanup Agent Don Quixote', 'Rarity000'],
            ['The Middle Little Sister Don Quixote', 'Rarity000'],
            ['Shi Assoc. South Section 5 Director Don Quixote', 'Rarity00'],
            ['Blade Lineage Salsu Don Quixote', 'Rarity00'],
            ['Lobotomy E.G.O::Lantern Don Quixote', 'Rarity00'],
            ['N Corp. Mittelhammer Don Quixote', 'Rarity00'],
            ['LCB Sinner Don Quixote', 'Rarity0'],
        ],
        EGOs: [
            ['La Sangre de Sancho', 'Z'],
            ['Lifetime Stew', 'T'],
            ['Electric Screaming', 'T'],
            ['Wishing Cairn', 'T'],
            ['Fluid Sac', 'H'],
            ['Telepole', 'H'],
        ],
    },
    RyoshuIDs: {
        IDs: [
            ['Edgar Family Chief Butler Ryoshu', 'Rarity000'],
            ['W Corp. L3 Cleanup Agent Ryoshu', 'Rarity000'],
            ['R.B. Chef de Cuisine Ryoshu', 'Rarity000'],
            ['Kurokumo Clan Wakashu Ryoshu', 'Rarity000'],
            ['Seven Assoc. South Section 6 Ryoshu', 'Rarity00'],
            ['LCCB Assistant Manager Ryoshu', 'Rarity00'],
            ['Liu Association South Section 4 Ryoshu', 'Rarity00'],
            ['LCB Sinner Ryoshu', 'Rarity0'],
        ],
        EGOs: [
            ['Forest for the Flames', 'Z'],
            ['Soda', 'ZnotOriginal'],
            ['Red Eyes', 'T'],
            ['Blind Obsession', 'T'],
            ['4th Match Flame', 'H'],
            ['Red Eyes (Open)', 'H'],
        ],
    },
    MeurIDs: {
        IDs: [
            ['Blade Lineage Mentor Meursault', 'Rarity000'],
            ['R Corp. 4th Pack Rhino Meursault', 'Rarity000'],
            ['N Corp. GroBHammer Meursault', 'Rarity000'],
            ['W Corp. L2 Cleanup Agent Meursault', 'Rarity000'],
            ['Liu Assoc. South Section 6 Meursault', 'Rarity00'],
            ['The Middle Little Brother Meursault', 'Rarity00'],
            ['Rosespanner Workshop Fixer Meursault', 'Rarity00'],
            ['Dead Rabbits Boss Meursault', 'Rarity00'],
            ['LCB Sinner Meursault', 'Rarity0'],
        ],
        EGOs: [
            ['Chains of Others', 'Z'],
            ['Screwloose Wallop', 'T'],
            ['Electric Screaming', 'T'],
            ['Regret', 'T'],
            ['Capote', 'H'],
            ['Pursuance', 'H'],
        ],
    },
    HongLuIDs: {
        IDs: [
            ['Ting Tang Gang Gangleader Hong Lu', 'Rarity000'],
            ['K Corp. Class 3 Excision Staff Hong Lu', 'Rarity000'],
            ['Dieci South Section 4 Hong Lu', 'Rarity000'],
            ['Kurokumo Clan Wakashu Hong Lu', 'Rarity00'],
            ['W Corp. L2 Cleanup Agent Hong Lu', 'Rarity00'],
            ['Liu Assoc. South Section 5 Hong Lu', 'Rarity00'],
            ['Hook Office Fixer Hong Lu', 'Rarity00'],
            ['LCB Sinner Hong Lu', 'Rarity0'],
        ],
        EGOs: [
            ['Land of Illusion', 'Z'],
            ['Roseate Desire', 'T'],
            ['Soda', 'T'],
            ['Dimension Shredder', 'H'],
            ['Effervescent Corrosion', 'H'],
        ],
    },
    HeathIDs: {
        IDs: [
            ['Öufi Association South Section 3 Heathcliff', 'Rarity000'],
            ['R Corp. 4th Pack Rabbit Heathcliff', 'Rarity000'],
            ['The Pequod Harpooneer Heathcliff', 'Rarity000'],
            ['Lobotomy E.G.O::Sunshower Heathcliff', 'Rarity000'],
            ['Shi Assoc. South Section 5 Heathcliff', 'Rarity00'],
            ['Seven Assoc. South Section 4 Heathcliff', 'Rarity00'],
            ['N Corp. Kleinhammer Heathcliff', 'Rarity00'],
            ['LCB Sinner Heathcliff', 'Rarity0'],
        ],
        EGOs: [
            ['Bodysack', 'Z'],
            ['Holiday', 'ZnotOriginal'],
            ['AEDD', 'T'],
            ['Ya Sunyata Tad Rupam', 'H'],
            ['Telepole', 'H'],
            ['Binds', 'W'],
        ],
    },
    IshIDs: {
        IDs: [
            ['The Pequod Captain Ishmael', 'Rarity000'],
            ['Molar Boatworks Fixer Ishmael', 'Rarity000'],
            ['R Corp. 4th Pack Reindeer Ishmael', 'Rarity000'],
            ['Liu Assoc. South Section 4 Ishmael', 'Rarity000'],
            ['Lobotomy E.G.O::Sloshing Ishmael', 'Rarity00'],
            ['Edgar Family Butler Ishmael', 'Rarity00'],
            ['Shi Assoc. South Section 5 Ishmael', 'Rarity00'],
            ['LCCB Assistant Manager Ishmael', 'Rarity00'],
            ['LCB Sinner Ishmael', 'Rarity0'],
        ],
        EGOs: [
            ['Snagharpoon', 'Z'],
            ['Roseate Desire', 'T'],
            ['Capote', 'T'],
            ['Ardor Blossom Star', 'H'],
            ['Wingbeat', 'H'],
            ['Blind Obsession', 'W'],
        ],
    },
    RodionIDs: {
        IDs: [
            ['Kurokumo Clan Wakashu Rodion', 'Rarity000'],
            ['Rosespanner Workshop Rep Rodion', 'Rarity000'],
            ['Dieci Assoc. South Section 4 Rodion', 'Rarity000'],
            ['Liu Association South Section 4 Director Rodion', 'Rarity000'],
            ['LCCB Assistant Manager Rodion', 'Rarity00'],
            ['Zwei Assoc. South Section 5 Rodion', 'Rarity00'],
            ['N Corp. Mittelhammer Rodion', 'Rarity00'],
            ['LCB Sinner Rodion', 'Rarity0'],
        ],
        EGOs: [
            ['What is Cast', 'Z'],
            ['Rime Shank', 'T'],
            ['Effervescent Corrosion', 'T'],
            ['4th Match Flame', 'H'],
            ['Pursuance', 'H'],
            ['Sanguine Desire', 'W'],
        ],
    },
    SinclairIDs: {
        IDs: [
            ['Dawn Office Fixer Sinclair', 'Rarity000'],
            ['Blade Lineage Salsu Sinclair', 'Rarity000'],
            ['Cinq Association South Section 4 Director Sinclair', 'Rarity000'],
            ['The One Who Shall Grip Sinclair', 'Rarity000'],
            ['Zwei Assoc. South Section 6 Sinclair', 'Rarity00'],
            ['Los Mariachis Jefe Sinclair', 'Rarity00'],
            ['Lobotomy E.G.O::Red Sheet Sinclair', 'Rarity00'],
            ['Molar Boatworks Fixer Sinclair', 'Rarity00'],
            ['LCB Sinner Sinclair', 'Rarity0'],
        ],
        EGOs: [
            ['Branch of Knowledge', 'Z'],
            ['Impending Day', 'T'],
            ['Lifetime Stew', 'T'],
            ['Lantern', 'H'],
            ['9:2', 'H'],
        ],
    },
    OutisIDs: {
        IDs: [
            ['Wuthering Heights Chief Butler Outis', 'Rarity000'],
            ['Seven Assoc. South Section 6 Director Outis', 'Rarity000'],
            ['Lobotomy E.G.O::Magic Bullet Outis', 'Rarity000'],
            ['Molar Office Fixer Outis', 'Rarity000'],
            ['G Corp. Head Manager Outis', 'Rarity00'],
            ['The Ring Pointillist Student Outis', 'Rarity00'],
            ['Blade Lineage Cutthroat Outis', 'Rarity00'],
            ['Cinq Association South Section 4 Outis', 'Rarity00'],
            ['LCB Sinner Outis', 'Rarity0'],
        ],
        EGOs: [
            ['To pathos Mathos', 'Z'],
            ['Sunshower', 'T'],
            ['Ya Sunyata Tad Rupam', 'T'],
            ['Ebony Stem', 'H'],
            ['Holiday', 'H'],
            ['Binds', 'W'],
        ],
    },
    GregorIDs: {
        IDs: [
            ['Edgar Family Heir Gregor', 'Rarity000'],
            ['G Corp. Manager Corporal Gregor', 'Rarity000'],
            ['Twinhook Pirates First Mate Gregor', 'Rarity000'],
            ['Zwei Assoc. South Section 4 Gregor', 'Rarity000'],
            ['Rosespanner Workshop Fixer Gregor', 'Rarity00'],
            ['Kurokumo Clan Captain Gregor', 'Rarity00'],
            ['Liu Assoc. South Section 6 Gregor', 'Rarity00'],
            ['R.B. Sous-chef Gregor', 'Rarity00'],
            ['LCB Sinner Gregor', 'Rarity0'],
        ],
        EGOs: [
            ['Suddenly,One Day', 'Z'],
            ['Legerdemain', 'ZnotOriginal'],
            ['AEDD', 'T'],
            ['Bygone Days', 'T'],
            ['Lantern', 'H'],
            ['Garden of Thorns', 'W'],
        ],
    },
};

export function createDefaultRosterProgress() {
    return Object.fromEntries(
        Object.entries(rosterCatalog).map(([sinnerKey, categories]) => [
            sinnerKey,
            {
                IDs: buildEntries(categories.IDs),
                EGOs: buildEntries(categories.EGOs),
            },
        ])
    );
}

export default createDefaultRosterProgress;