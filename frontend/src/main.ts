import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppComponent } from './app/app.component'; // Załóżmy, że masz plik AppModule
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { JwtModule } from '@auth0/angular-jwt';

export function tokenGetter() {
  return localStorage.getItem('token');
}

platformBrowserDynamic().bootstrapModule(AppModule, {
  providers: [
    HttpClientModule,
    RouterModule.forRoot([]), // tutaj możesz dodać swoje ścieżki
    JwtModule.forRoot({
      config: {
        tokenGetter: tokenGetter,
        allowedDomains: ['localhost'],
        disallowedRoutes: ['/api/auth/login', '/api/auth/register']
      }
    })
  ]
}).catch(err => console.error(err));
