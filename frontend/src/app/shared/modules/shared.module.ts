import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { TranslateModule } from "@ngx-translate/core";
import { IconsProviderModule } from "@app/providers/icons-provider.module";
import { NgZorroModule } from "./ng-zorro.module";
import { LanguageSwitcherComponent } from '../components/language-switcher/language-switcher.component';
import { ScrollingModule } from "@angular/cdk/scrolling";
//import { CurrencyPricePipe } from '../pipes/currency-price/currency-price.pipe';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    NgZorroModule,
    TranslateModule,
    IconsProviderModule,
    ScrollingModule,
  ],
  exports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    NgZorroModule,
    TranslateModule,
    IconsProviderModule,
    LanguageSwitcherComponent,
    ScrollingModule,
   // CurrencyPricePipe,
  ],
  declarations: [
    LanguageSwitcherComponent,
    // CurrencyPricePipe,
  ],
})
export class SharedModule { }
