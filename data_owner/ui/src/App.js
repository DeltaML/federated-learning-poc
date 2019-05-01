import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Typing from 'react-typing-animation';
import CircularIntegration from './circular-integration/circular-integration';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <Typing>
            <code>Hey there!</code>
            <br/>
            <code>You can load your dataset here.</code>
          </Typing>
          <CircularIntegration />
        </header>
      </div>
    );
  }
}

export default App;
