import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AventureComponent } from './aventure/aventure.component';
import { CarsComponent } from './cars/cars.component';
import { CircuitComponent } from './circuit/circuit.component';
import { HomeComponent } from './home.component';
import { UsersComponent } from './users/users.component';

const routes: Routes = [
  { path: '',
   component: HomeComponent,
  children: [
    {
      path: '', pathMatch: 'full',
      redirectTo: '/home/users',
    },
    {
      path: 'users',
      component: UsersComponent,
      data: { breadcrumb: 'admin.home.users.title' },
    },
    {
      path: 'cars',
      component: CarsComponent,
      data: { breadcrumb: 'admin.home.users.title' },
    },
    {
      path: 'aventure',
      component: AventureComponent,
      data: { breadcrumb: 'admin.home.users.title' },
    },
    {
      path: 'circuit',
      component: CircuitComponent,
      data: { breadcrumb: 'admin.home.users.title' },
    },
  ]
 },
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomeRoutingModule {
}





