import './App.css'

function App() {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
  const prettyTgData = JSON.stringify(window.Telegram.WebApp.initDataUnsafe, undefined, 2);

  return (
    <>
      <div>
        {prettyTgData}
      </div>
    </>
  )
}

export default App
