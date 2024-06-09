import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter, withInMemoryScrolling } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { importProvidersFrom } from '@angular/core';
import { JwtModule } from '@auth0/angular-jwt';

import { AppComponent } from './app/app.component';
import { LoginComponent } from './app/auth/login/login.component';
import { RegisterComponent } from './app/auth/register/register.component';
import { ChatComponent } from './app/chat/chat.component';

export function tokenGetter() {
  return localStorage.getItem('token');
}

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(
      [
        { path: 'login', component: LoginComponent },
        { path: 'register', component: RegisterComponent },
        { path: 'chat', component: ChatComponent },
        { path: '', redirectTo: '/login', pathMatch: 'full' }
      ],
      withInMemoryScrolling({ anchorScrolling: 'enabled' })
    ),
    provideHttpClient(),
    provideAnimations(),
    importProvidersFrom(
      JwtModule.forRoot({
        config: {
          tokenGetter: tokenGetter,
          allowedDomains: ['localhost:8080'],
          disallowedRoutes: ['http://localhost:8080/api/auth/login', 'http://localhost:8080/api/auth/register']
        }
      })
    )
  ]
}).catch(err => console.error(err));
