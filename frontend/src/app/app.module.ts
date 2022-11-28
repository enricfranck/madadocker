import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BreadcrumbModule } from 'xng-breadcrumb';

import { TranslationProviderModule } from './providers/translation-provider.module';
import { SharedModule } from './shared/modules/shared.module';
import { ErrorInterceptor, JwtInterceptor } from './helpers';
import { fakeApiProvider } from './providers/fake-api-provider.module';

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    TranslationProviderModule,
    SharedModule,
    BreadcrumbModule,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    fakeApiProvider,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
