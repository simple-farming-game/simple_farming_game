using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

using MonoGame.Extended.Tiled;
using MonoGame.Extended.Tiled.Renderers;

namespace simple_farming_game
{
    public class Game1 : Game
    {
        Texture2D playerTexture;
        Vector2 playerPosition;
        float playerSpeed;

        private GraphicsDeviceManager _graphics;
        private SpriteBatch _spriteBatch;

        TiledMap _tiledMap;
        TiledMapRenderer _tiledMapRenderer;

        public Game1()
        {
            _graphics = new GraphicsDeviceManager(this);
            Content.RootDirectory = "Content";
            IsMouseVisible = true;
        }

        protected override void Initialize()
        {
            // TODO: Add your initialization logic here
            playerPosition = new Vector2(_graphics.PreferredBackBufferWidth / 2,_graphics.PreferredBackBufferHeight / 2);
            playerSpeed = 550f;

            base.Initialize();
        }

        protected override void LoadContent()
        {
            _tiledMap = Content.Load<TiledMap>("samplemap");
            _tiledMapRenderer = new TiledMapRenderer(GraphicsDevice, _tiledMap);

            _spriteBatch = new SpriteBatch(GraphicsDevice);
        }

        protected override void Update(GameTime gameTime)
        {
            _tiledMapRenderer.Update(gameTime);
        }

        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.Black);

            _tiledMapRenderer.Draw();
        }
    }
}