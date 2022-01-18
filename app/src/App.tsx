import React from "react";
import { Provider } from "mobx-react";
import Editor from "rich-markdown-editor";

import stores from "./stores";

import "./App.css";

const App: React.FC = () => {
  return (
    <Provider {...stores}>
      <div style={{ margin: "25px" }}>
        <Editor defaultValue="Hello world!" />
      </div>
    </Provider>
  );
};

export default App;
