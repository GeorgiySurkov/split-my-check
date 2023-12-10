import type React from 'react';

import {WebAppProvider} from "@vkruglikov/react-telegram-web-app";
import {ExpenseGroupPage} from "src/pages/expense_group";
import {SafeTgInitDataProvider} from "src/shared/lib/safe_tg_init_data";

export const App: React.FC = () => {
  return (
    <WebAppProvider options={{smoothButtonsTransition: true}}>
        <SafeTgInitDataProvider>
            <ExpenseGroupPage/>
        </SafeTgInitDataProvider>
    </WebAppProvider>
  )
}
