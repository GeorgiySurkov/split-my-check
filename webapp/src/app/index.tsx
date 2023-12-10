import type React from 'react';

import './index.css'
import {WebAppProvider} from "@vkruglikov/react-telegram-web-app";
import {ExpenseGroupPage} from "src/pages/expense_group";

export const App: React.FC = () => {
  return (
    <WebAppProvider options={{smoothButtonsTransition: true}}>
      <ExpenseGroupPage/>
    </WebAppProvider>
  )
}
