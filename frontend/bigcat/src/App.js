import logo from './logo.svg';
import './App.css';
import Form from './components/Login';

function App() {
  return (
    <div className='w-full flex h-screen justify-center'>
      <div className='w-full flex items-center justify-center lg:w-1/2'>
        <Form/>
      </div>
    </div>
  );
}

export default App;
