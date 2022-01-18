import { MobXProviderContext } from "mobx-react";
import React from "react";
import { IRootStore } from "../stores/RootStore";

export default function useStores(): IRootStore {
  return React.useContext(MobXProviderContext);
}
