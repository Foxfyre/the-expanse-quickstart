Hooks.on("init", () => {
    game.settings.register("the-expanse-quickstart", "initialized", {
        name: "Initialization",
        scope: "world",
        config: false,
        default: false,
        type: Boolean
    });

    game.settings.registerMenu("the-expanse-quickstart", "init-dialogue", {
        name: "The Expanse Quickstart Setup",
        label: "Setup",
        hint: "Import or update the content from The Expanse Quickstart Module",
        type: TheExpanseQSInitWrapper,
        restricted: true
    })
})

Hooks.on("ready", () => {
    if (!game.settings.get("the-expanse-quickstart", "initialized") && game.user.isGM) {
        new TheExpanseQSInitialization().render(true)
    }
})

class TheExpanseQSInitWrapper extends FormApplication {
    render() {
        new TheExpanseQSInitialization().render(true);
    }
}
 
class TheExpanseQSInitialization extends Dialog {
    constructor() {
        super({
            title: "The Expanse Quickstart Initialization",
            content: `<div class="popup"><h1>The Expanse - Quickstart</h1>
            <p>Green Ronin Publishing is proud to present the Foundry module of The Quickstart for <i>The Expanse RPG</i>! In this module, you will find everything you need to get started with your first game of The Expanse RPG.</p>
            <h2>Contents</h2>
            <ul>
            <li><b>6 Pregen Characters</li>
            <li>6 NPCs</li>
            <li>Weapons</li>
            <li>Talents</li>
            <li>Stunts</li>
            <li>Introductory Rules</li>
            <li>The Cupbearer Starter Adventure</li>
            <li>The Churn Tracker and Ship Tracking Scenes</b></li>
            </ul>
            <h2></h2>
            
            No part of this publication may be reproduced, distributed, stored in a retrieval system, or transmitted in any form by any means, electronic, mechanical, photocopying, recording or otherwise without the prior permission of the publishers.<br><br>

            <p><i>The Expanse Roleplaying Game</i> is ©2019 Green Ronin Publishing, LLC. All rights reserved. First Printing. References to other copyrighted material
            in no way constitute a challenge to the respective copyright holders of that material. Green Ronin, <i>The Expanse Roleplaying Game</i>,
            and their associated logos are trademarks of Green Ronin Publishing, LLC. The Expanse is © 2011-2019 Daniel Abraham and Ty Franck.</br>
            <div class="popup-img"><img src="modules/the-expanse-quickstart/images/roninlogo02_color300.png" width="69" height="120" />    <img src="modules/the-expanse-quickstart/images/AGE_logo_Expanse.png" width="161" height="100" /></div><br><br>

            Published by:<b>Green Ronin Publishing</b>
            Foundry System by:<b>Charlotte Hamilton (Foxfyre)</b><br>

            <a href="mailto:letsplay@greenronin.com"></a>
            
            </br>
            <b>Initialize Module to import all content?</b></div>
            `,
            module: game.modules.get("the-expanse-quickstart"),
            buttons: {
                initialize: {
                    label: "Initialize",
                    callback: async () => {
                        game.settings.set("the-expanse-quickstart", "initialized", true)
                        await new TheExpanseQSInitialization().initialize()
                        ui.notifications.notify("Initialization Complete")
                    }
                },
                update: {
                    label: "Update",
                    callback: async () => {
                        let updater = await game.the - TheExpanseQSInitialization.apps.ModuleUpdater.create(game.modules.get("the-expanse-quickstart"), this)
                        updater.render(true)
                    }
                },
                no: {
                    label: "No",
                    callback: () => {
                        game.settings.set("the-expanse-quickstart", "initialized", true)
                        ui.notifications.notify("Skipped Initialization.")
                    }
                }
            }
        })

        this.folders = {
            "Scene": {},
            "Item": {},
            "Actor": {},
            "JournalEntry": {}
        }

        this.journals = {};
        this.actors = {};
        this.items = {};
        this.scenes = {};
        this.moduleKey = "the-expanse-quickstart";
    }

    async initialize() {
        return new Promise((resolve) => {
            fetch(`modules/${this.moduleKey}/initialization.json`).then(async r => r.json()).then(async json => {
                let createdFolders = await Folder.create(json)
                for (let folder of createdFolders)
                    this.folders[folder.data.type][folder.data.name] = folder;

                for (let folderType in this.folders) {
                    for (let folder in this.folders[folderType]) {

                        let parent = this.folders[folderType][folder].getFlag(this.moduleKey, "initialization-parent")
                        if (parent) {
                            let parentId = this.folders[folderType][parent].id
                            await this.folders[folderType][folder].update({ parent: parentId })
                        }
                    }
                }

                await this.initializeEntities()
                /* This need's to be turned on when scenes are present */
                await this.initializeScenes()
                resolve()

            })
        })
    }

    async initializeEntities() {

        let packList = this.data.module.data.flags.initializationPacks
        console.log(packList);
        for (let pack of packList) {
            console.log(pack);
                    if (game.packs.get(pack).metadata.entity == "Scene")
                continue
            let documents = await game.packs.get(pack).getDocuments();
            console.log(documents);
            for (let document of documents) {
                console.log(document);
                let folder = document.getFlag(this.moduleKey, "initialization-folder")
                console.log(folder);
                if (folder)
                    document.data.update({ "folder": this.folders[document.documentName][folder].id })
                if (document.data.flags[this.moduleKey].sort)
                    document.data.update({ "sort": document.data.flags[this.moduleKey].sort })
            }
            switch (documents[0].documentName) {
                case "Actor":
                    ui.notifications.notify("Initializing Actors")
                    await Actor.create(documents.map(c => c.data))
                    break;
                case "Item":
                    ui.notifications.notify("Initializing Items")
                    await Item.create(documents.map(c => c.data))
                    break;
                case "JournalEntry":
                    ui.notifications.notify("Initializing Journals")
                    let createdEntries = await JournalEntry.create(documents.map(c => c.data))
                    for (let entry of createdEntries)
                        this.journals[entry.data.name] = entry
                    break;
            }
        }
    }


     /*This need's to be turned one when there are scenes to import */
    async initializeScenes() {
        ui.notifications.notify("Initializing Scenes")
        let m = game.packs.get(`${this.moduleKey}.scenes-quickstart`)
        let maps = await m.getDocuments()
        for (let map of maps) {
            let folder = map.getFlag(this.moduleKey, "initialization-folder")
            if (folder)
                map.data.update({ "folder": this.folders["Scene"][folder].id })
        }
        await Scene.create(maps.map(m => m.data)).then(sceneArray => {
            sceneArray.forEach(async s => {
                let thumb = await s.createThumbnail();
                s.update({ "thumb": thumb.thumb })
            })
        })
    }
}

class TheExpanseQSInitializationSetup {
    static async setup () {
        TheExpanseQSInitializationSetup.displayFolders();
        TheExpanseQSInitializationSetup.setFolderFlags();
        TheExpanseQSInitializationSetup.setSceneNotes();
        TheExpanseQSInitializationSetup.setEmbeddedEntities();
    }

    static async displayFolders() {
        let array = [];
        game.folders.entities.forEach(async f => {
            if (f.data.parent)
                await f.setFlag("the-expanse-quickstart", "initialization-parent", game.folders.get(f.data.parent).data.name)
        })
        game.folders.entities.forEach(f => {
            array.push(f.data);
        })
        console.log(JSON.stringify(array))
    }

    static async setFolderFlags() {
        for (let scene of game.scenes.entities)
            await scene.update({ "flags.the-expanse-quickstart": { "initialization-folder": game.folders.get(scene.data.folder).data.name, sort: scene.data.sort } })
        for (let actor of game.actors.entities)
            await actor.update({ "flags.the-expanse-quickstart": { "initialization-folder": game.folders.get(actor.data.folder).data.name, sort: actor.data.sort } })
        for (let item of game.items.entities)
            await item.update({ "flags.the-expanse-quickstart": { "initialization-folder": game.folders.get(item.data.folder).data.name, sort: item.data.sort } })
        for (let journal of game.journal.entities)
            await journal.update({ "flags.the-expanse-quickstart": { "initialization-folder": game.folders.get(journal.data.folder)?.data?.name, sort: journal.data.sort } })
    }

    static async setSceneNotes() {
        for (let scene of game.scenes.entities)
            if (scene.data.journal)
                await scene.setFlag("the-expanse-quickstart", "scene-notes", game.journal.get(scene.data.journal).data.name)
    }

    static async setEmbeddedEntities() {
        for (let scene of game.scenes.entities) {
            let notes = duplicate(scene.data.notes)
            for (let note of notes) {
                setProperty(note, "flags.the-expanse-quickstart.initialization-entryname", game.journal.get(note.entryId).data.name)
            }
            await scene.update({ notes: notes })
        }
    }
}