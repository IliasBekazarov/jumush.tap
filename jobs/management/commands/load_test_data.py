from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Category, Job
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Тест маалыматтарды базага кошот'

    def handle(self, *args, **kwargs):
        self.stdout.write('Тест маалыматтарды кошуу башталды...')
        
        # Категорияларды түзүү
        categories_data = [
            {'name': 'Үй жумуштары', 'icon': 'fa-home'},
            {'name': 'Транспорт', 'icon': 'fa-car'},
            {'name': 'Оңдоо', 'icon': 'fa-wrench'},
            {'name': 'Окутуу', 'icon': 'fa-book'},
            {'name': 'IT кызматтар', 'icon': 'fa-laptop'},
            {'name': 'Тамак-аш', 'icon': 'fa-utensils'},
            {'name': 'Айыл чарба', 'icon': 'fa-seedling'},
            {'name': 'Дизайн', 'icon': 'fa-palette'},
            {'name': 'Фото/Видео', 'icon': 'fa-camera'},
            {'name': 'Курулуш', 'icon': 'fa-hard-hat'},
        ]
        
        for cat_data in categories_data:
            # Slug кол менен түзөбүз
            from django.utils.text import slugify
            slug = slugify(cat_data['name'])
            
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon']
                }
            )
            if created:
                self.stdout.write(f'✓ Категория түзүлдү: {category.name}')
        
        # Тест колдонуучуларды түзүү
        test_users = []
        for i in range(1, 4):
            username = f'user{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@test.com',
                    'first_name': f'Колдонуучу{i}',
                    'last_name': f'Тест{i}'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'✓ Колдонуучу түзүлдү: {username}')
            
            # Профилди жаңыртуу
            profile = user.profile
            profile.user_type = ['seeker', 'employer', 'both'][i-1]
            profile.phone = f'+996 555 {i}00 {i}00'
            profile.location = ['Бишкек', 'Ош', 'Жалал-Абад'][i-1]
            profile.bio = f'Мен {username}, жумуш издеп жүрөм'
            profile.save()
            
            test_users.append(user)
        
        # Тест жумуштарды түзүү
        jobs_data = [
            {
                'title': 'Үй тазалоо керек',
                'description': '3 бөлмөлүү үйдү тазалап берүү керек. Жума күнү, таңкы 10:00дөн. Жалпы 3-4 саат убакыт алат.',
                'category': 'Үй жумуштары',
                'job_type': 'onetime',
                'price': 1500,
                'location': 'Бишкек, Ала-Тоо район',
            },
            {
                'title': 'Математика окутуучу керек',
                'description': '7-класс окуучу үчүн математика боюнча сабак берүүчү керек. Жумасына 3 жолу, бир сааттан.',
                'category': 'Окутуу',
                'job_type': 'parttime',
                'price': 300,
                'location': 'Бишкек, Асанбай',
            },
            {
                'title': 'Веб-сайт керек',
                'description': 'Чакан бизнес үчүн жөнөкөй веб-сайт жасатуу керек. Дизайн жана программалоо. Эң көп 5 барак.',
                'category': 'IT кызматтар',
                'job_type': 'onetime',
                'price': 15000,
                'location': 'Бишкек',
            },
            {
                'title': 'Жүк ташуу (1 тонна)',
                'description': 'Эмерек ташыш керек, Орто-Сай айылынан Бишкекке. 1 тонна чамасы. Машина менен.',
                'category': 'Транспорт',
                'job_type': 'onetime',
                'price': 5000,
                'location': 'Чүй областы',
            },
            {
                'title': 'Кран оңдоо',
                'description': 'Ашканадагы кран агып жатат, оңдоп берүү керек. Тез арада.',
                'category': 'Оңдоо',
                'job_type': 'onetime',
                'price': 500,
                'location': 'Бишкек, Кок-Жар',
            },
            {
                'title': 'Күнүмдүк ашпоз керек',
                'description': 'Кафеге ашпоз керек. 9:00дөн 18:00гө чейин. Кыргыз тамактарын бышыра билүү шарт.',
                'category': 'Тамак-аш',
                'job_type': 'fulltime',
                'price': 25000,
                'location': 'Ош шаары',
            },
            {
                'title': 'Баг оңдоо',
                'description': 'Жазгы коттеджде бак-дарактарды кесүү, чөп чабуу керек. 1 күнгө жумуш.',
                'category': 'Айыл чарба',
                'job_type': 'daily',
                'price': 2000,
                'location': 'Ысык-Көл, Чолпон-Ата',
            },
            {
                'title': 'Логотип дизайны',
                'description': 'Жаңы ачылган кафе үчүн логотип жасатуу керек. Заманбап стилде.',
                'category': 'Дизайн',
                'job_type': 'onetime',
                'price': 3000,
                'location': 'Бишкек',
            },
            {
                'title': 'Той тартуу (фото+видео)',
                'description': 'Үйлөнүү тоюна фото жана видео тартып берүү керек. Камыл келүү күнү.',
                'category': 'Фото/Видео',
                'job_type': 'onetime',
                'price': 12000,
                'location': 'Жалал-Абад',
            },
            {
                'title': 'Үй куруу',
                'description': 'Кыштак жеринде чакан үй (70 кв.м) салдыруу керек. Материалдар бар.',
                'category': 'Курулуш',
                'job_type': 'fulltime',
                'price': 250000,
                'location': 'Талас области',
            },
        ]
        
        for job_data in jobs_data:
            try:
                category = Category.objects.get(name=job_data['category'])
            except Category.DoesNotExist:
                # Эгер категория жок болсо, биринчи категорияны алабыз
                category = Category.objects.first()
            
            employer = test_users[0]  # Биринчи колдонуучу бардык жумуштарды жарыялайт
            
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                defaults={
                    'description': job_data['description'],
                    'category': category,
                    'job_type': job_data['job_type'],
                    'price': job_data['price'],
                    'location': job_data['location'],
                    'employer': employer,
                    'contact_phone': '+996 555 100 100',
                    'status': 'active'
                }
            )
            if created:
                self.stdout.write(f'✓ Жумуш түзүлдү: {job.title}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Тест маалыматтар ийгиликтүү кошулду!'))
        self.stdout.write('\n📝 Колдонуучулар:')
        self.stdout.write('   - user1 / password123')
        self.stdout.write('   - user2 / password123')
        self.stdout.write('   - user3 / password123')
        self.stdout.write('\n🎯 Админ панель: http://127.0.0.1:8000/admin')
        self.stdout.write('   - admin / admin123\n')
