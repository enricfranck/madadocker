import { NgModule } from '@angular/core';
import { HomeRoutingModule } from './home-routing.module';
import { HomeComponent } from './home.component';
import { SharedModule } from '@app/shared/modules/shared.module';
import { UsersComponent } from './users/users.component';
import { CarsComponent } from './cars/cars.component';
import { AventureComponent } from './aventure/aventure.component';
import { CircuitComponent } from './circuit/circuit.component';

@NgModule({
  declarations: [HomeComponent, UsersComponent, CarsComponent, AventureComponent, CircuitComponent],
  imports: [SharedModule, HomeRoutingModule],
})
export class HomeModule { }