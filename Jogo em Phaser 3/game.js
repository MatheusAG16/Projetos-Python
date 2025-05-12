const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 300 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

function preload() {
    this.load.image('sky', 'https://labs.phaser.io/assets/skies/space3.png');
    this.load.image('ground', 'https://labs.phaser.io/assets/sprites/platform.png');
    this.load.image('star', 'https://labs.phaser.io/assets/demoscene/star.png');
    this.load.spritesheet('dude', 'https://labs.phaser.io/assets/sprites/dude.png', { frameWidth: 32, frameHeight: 48 });
}

function create() {
    this.add.image(400, 300, 'sky');
    const platforms = this.physics.add.staticGroup();
    platforms.create(400, 568, 'ground').setScale(2).refreshBody();
}

function update() {
    // Lógica do jogo
}