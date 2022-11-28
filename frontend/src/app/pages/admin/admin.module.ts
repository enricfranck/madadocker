import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/modules/shared.module';
import { BreadcrumbModule } from 'xng-breadcrumb';
import { AdminRoutingModule } from './admin-routing.module';
import { AdminComponent } from './admin.component';
import { MenuComponent } from '@app/components/menu/menu.component';
import { ProfilDropdownComponent } from '@app/components/profil-dropdown/profil-dropdown.component';
import { LanguageSelectComponent } from '@app/components/select/language-select/language-select.component';

@NgModule({
  declarations: [
    MenuComponent,
    LanguageSelectComponent,
    ProfilDropdownComponent,
    AdminComponent,
  ],
  imports: [
    SharedModule,
    BreadcrumbModule,
    AdminRoutingModule,
  ],
  bootstrap: [
    AdminComponent
  ]
})
export class AdminModule { }
