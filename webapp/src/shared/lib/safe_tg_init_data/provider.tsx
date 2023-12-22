import React from "react";

import WebApp from "@twa-dev/sdk";
import useSWR from "swr";

import {SafeTgInitDataContext} from "./context";
import type {SafeTgInitData} from "./types";

export const SafeTgInitDataProvider: React.FC<{ children?: React.ReactNode }> = ({children}) => {

    const {isLoading, data: safeInitData, error} = useSWR<SafeTgInitData, Error>(
        `${import.meta.env.VITE_API_BASE_URL}/validate_init_data?${WebApp.initData}`,
        async (url: string) => {
            const response = await fetch(url);
            if (!response.ok) throw new Error("Failed to fetch safe init data");
            const res = await response.json() as SafeTgInitData;
            console.log("received safe init data", res);
            return res;
        },
        {revalidateOnFocus: false}
    );

    let wrappedChildren = children;
    if (isLoading) {
        wrappedChildren = <div>Loading...</div>;
    } else if (error) {
        // const prettyError = JSON.stringify(error, null, 2);
        wrappedChildren = <div>Error: {error.message}</div>;
    }

    return (
        <SafeTgInitDataContext.Provider value={safeInitData ?? null}>
            {wrappedChildren}
        </SafeTgInitDataContext.Provider>
    );
}
