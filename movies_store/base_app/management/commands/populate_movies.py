from django.core.management.base import BaseCommand
from base_app.models import Movie

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(Movie.objects.all()) != 0:
            self.stdout.write(self.style.WARNING("Movie table already populated"))
            return
        Movie.objects.create(title="The Shawshank Redemption", category="Drama",
                             rating=9.3, details="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.")
        Movie.objects.create(title="The Lord of the Rings: The Return of the King",
                             category="Fantasy", rating=9.0, details="Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.")
        Movie.objects.create(title="The Godfather", category="Crime",
                             rating=9.2, details="The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son.")
        Movie.objects.create(title="The Dark Knight", category="Superhero",
                             rating=9.1, details="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.")
        Movie.objects.create(title="Pulp Fiction", category="Crime",
                             rating=8.9, details="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.")
        Movie.objects.create(title="Inception", category="Sci-Fi",
                             rating=8.8, details="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster.")
        Movie.objects.create(title="Fight Club", category="Drama",
                             rating=8.8, details="An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.")
        Movie.objects.create(title="Forrest Gump", category="Drama",
                             rating=8.8, details="The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.")
        Movie.objects.create(title="The Matrix", category="Action",
                             rating=9.1, details="When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.")
        Movie.objects.create(title="Interstellar", category="Drama",
                             rating=8.7, details="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.")
        Movie.objects.create(title="Star Wars Episode V", category="Fantasy",
                             rating=8.7, details="After the Rebels are brutally overpowered by the Empire on the ice planet Hoth, Luke Skywalker begins Jedi training with Yoda, while his friends are pursued across the galaxy by Darth Vader and bounty hunter Boba Fett.")
        Movie.objects.create(title="The Green Mile", category="Drama",
                             rating=8.6, details="The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift.")
        Movie.objects.create(title="Se7en", category="Crime",
                             rating=8.6, details="Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.")
        Movie.objects.create(title="Terminator 2", category="Action",
                             rating=8.6, details="A cyborg, identical to the one who failed to kill Sarah Connor, must now protect her ten-year-old son John from a more advanced and powerful cyborg.")
        Movie.objects.create(title="The Silence of the Lambs", category="Crime",
                             rating=8.6, details="A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims.")
        Movie.objects.create(title="Back to the Future", category="Sci-Fi",
                             rating=8.6, details="Marty McFly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling DeLorean invented by his close friend, the eccentric scientist Doc Brown.")
        Movie.objects.create(title="Star Wars Episode IV", category="Fantasy",
                             rating=8.6, details="Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station, while also attempting to rescue Princess Leia from the mysterious Darth Vader.")
        Movie.objects.create(title="Avengers: Infinity War", category="Superhero",
                             rating=8.5, details="The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.")
        Movie.objects.create(title="Django Unchained", category="Drama",
                             rating=8.5, details="With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal plantation-owner in Mississippi.")
        Movie.objects.create(title="Spider-Man: No Way Home", category="Superhero",
                             rating=8.5, details="With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other what it truly means to be Spider-Man.")
        self.stdout.write(self.style.SUCCESS("Successfully populated the Movie table"))
