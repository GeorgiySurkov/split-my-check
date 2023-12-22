import React from "react";

import {useLocation} from "react-router-dom";
import {TgRoutingBackButton} from "./TgRoutingBackButton.component.tsx";


export const TgRoutingWrapper: React.FC<React.PropsWithChildren> = ({children}) => {
  const location = useLocation();
  const doesAnyHistoryEntryExist = location.key !== "default";

  return (
    <>
      {doesAnyHistoryEntryExist && <TgRoutingBackButton/>}
      {children}
    </>
  )
}
