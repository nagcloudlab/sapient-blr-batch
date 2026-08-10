
const EventEmitter = require('events');


//---------------------------------------------
// Door module
//---------------------------------------------

class Door extends EventEmitter {
    open() {
        console.log('Door is opened');
        this.emit('door-open', { floor: 4, room: "Vallbha" });
    }
    close() {
        console.log('Door is closed')
        this.emit('door-close', { floor: 4, room: "Vallbha" });
    }
}

const door = new Door();


//---------------------------------------------
// Light module
//---------------------------------------------

door.on('door-open', (event) => {
    console.log(`Light is ON for ${event.floor} floor and ${event.room} room`);
});

door.on('door-close', (event) => {
    console.log(`Light is OFF for ${event.floor} floor and ${event.room} room`);
});


//---------------------------------------------
// Projector module
//---------------------------------------------

door.on('door-open', (event) => {
    console.log(`Projector is ON for ${event.floor} floor and ${event.room} room`);
});

door.on('door-close', (event) => {
    console.log(`Projector is OFF for ${event.floor} floor and ${event.room} room`);
});




setTimeout(() => {
    door.open();
    setTimeout(() => {
        door.close();
    }, 2000);
}, 2000);


