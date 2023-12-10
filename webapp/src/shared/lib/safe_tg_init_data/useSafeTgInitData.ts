import React from "react";
import {SafeTgInitData} from "./types";
import {SafeTgInitDataContext} from "./context";

export function useSafeTgInitData(): SafeTgInitData {
    const initData = React.useContext(SafeTgInitDataContext);
    if (initData === null) {
        throw new Error("useSafeTgInitData must be used within a SafeTgInitDataProvider");
    }
    return initData;
}
