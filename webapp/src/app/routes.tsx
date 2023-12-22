import {createMemoryRouter} from "react-router-dom";

import {ExpenseGroupPage} from "src/pages/expense_group";
import {EditExpenseGroupPage} from "src/pages/exit_expense_group";
import {TgRoutingWrapper} from "src/shared/lib/tg_routing";


export const router = createMemoryRouter([
  {
    path: '',
    element: <TgRoutingWrapper><ExpenseGroupPage/></TgRoutingWrapper>,
  },
  {
    path: '/edit',
    element: <TgRoutingWrapper><EditExpenseGroupPage/></TgRoutingWrapper>,
  },
]);
