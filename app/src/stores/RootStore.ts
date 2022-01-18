import UIStore from "./UIStore";

export interface IRootStore {
  ui?: UIStore;
}

export default class RootStore implements IRootStore {
  ui: UIStore;

  constructor() {
    this.ui = new UIStore();
  }

  get stores() {
    return {
      ui: this.ui
    };
  }
}
