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
            _spriteBatch = new SpriteBatch(GraphicsDevice);

            // TODO: use this.Content to load your game content here
            playerTexture = Content.Load<Texture2D>("player");

            _tiledMap = Content.Load<TiledMap>("tiledmap1");
            _tiledMapRenderer = new TiledMapRenderer(GraphicsDevice, _tiledMap);

            _spriteBatch = new SpriteBatch(GraphicsDevice);
        }

        protected override void Update(GameTime gameTime)
        {
            if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed || Keyboard.GetState().IsKeyDown(Keys.Escape))
                Exit();

            // TODO: Add your update logic here
            var kstate = Keyboard.GetState();

            if (kstate.IsKeyDown(Keys.W))
            {
                playerPosition.Y -= playerSpeed * (float)gameTime.ElapsedGameTime.TotalSeconds;
            }

            if (kstate.IsKeyDown(Keys.S))
            {
                playerPosition.Y += playerSpeed * (float)gameTime.ElapsedGameTime.TotalSeconds;
            }

            if (kstate.IsKeyDown(Keys.A))
            {
                playerPosition.X -= playerSpeed * (float)gameTime.ElapsedGameTime.TotalSeconds;
            }

            if (kstate.IsKeyDown(Keys.D))
            {
                playerPosition.X += playerSpeed * (float)gameTime.ElapsedGameTime.TotalSeconds;
            }
            _tiledMapRenderer.Update(gameTime);
            base.Update(gameTime);
        }

        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.CornflowerBlue);

            // TODO: Add your drawing code here

            _tiledMapRenderer.Draw();

            _spriteBatch.Begin();
            _spriteBatch.Draw(
                playerTexture,
                playerPosition,
                null,
                Color.White,
                0f,
                new Vector2(playerTexture.Width / 2, playerTexture.Height / 2),
                Vector2.One,
                SpriteEffects.None,
                0f
            );
            _spriteBatch.End();

            base.Draw(gameTime);
        }
    }
}