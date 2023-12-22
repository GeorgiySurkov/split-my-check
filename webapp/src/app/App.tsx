import type React from "react";
import {RouterProvider} from "react-router-dom";
import {SafeTgInitDataProvider} from "src/shared/lib/safe_tg_init_data";
import {router} from "./routes.tsx";


export const App: React.FC = () => {
  return (
    <SafeTgInitDataProvider>
      <RouterProvider router={router}/>
      {/*<TgRoutingBackButton/>*/}
    </SafeTgInitDataProvider>
  )
}
